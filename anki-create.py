"""Main application entry point."""

import argparse
import logging
import os
import sys
import warnings

from tqdm import tqdm

from src.card_creator import CardCreator
from src.config import LANGUAGES
from src.llm_client import LLMClient
from src.user_interface import UserInterface

# Configuration globale pour supprimer tous les avertissements transformers
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Crée des cartes Anki avec définition, synonymes et exemples audio pour des mots étrangers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python anki-create.py "hello"                           # Crée une carte pour le mot anglais "hello"
  python anki-create.py "hello; goodbye; you nail it!"    # Crée plusieurs cartes à la fois
  python anki-create.py "hola" "espagnol"                 # Crée une carte pour le mot espagnol "hola"
  python anki-create.py "こんにちは" "japonais"              # Crée une carte pour le mot japonais "こんにちは"
  python anki-create.py "hello; goodbye" -y               # Accepte automatiquement la réponse du LLM
        """)

    parser.add_argument(
        "words", nargs="?", help="Le(s) mot(s) étranger(s) pour lesquel(s) créer une carte Anki (séparés par des points-virgules)")
    parser.add_argument("language", nargs="?", default="Anglais",
                        help="La langue du mot fourni et nom du deck Anki (défaut: Anglais)")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="Accepte automatiquement la réponse du LLM sans demander confirmation")

    return parser.parse_args()


def main():
    """Main application logic."""
    args = parse_arguments()
    ui = UserInterface()

    # Validate input
    if not args.words:
        ui.show_available_languages(LANGUAGES)
        sys.exit(1)

    # Parse multiple words separated by semicolons
    words_list = [word.strip() for word in args.words.split(';')]
    source_language = args.language.capitalize()

    # Show connection status
    ui.show_anki_connection_status()

    # Initialize components
    llm_client = LLMClient()
    card_creator = CardCreator()

    # Process each word
    total_words = len(words_list)
    ui.show_processing_start(total_words)

    for word_index, word in enumerate(words_list, 1):
        if not word:  # Skip empty strings
            continue

        ui.show_word_progress(word, word_index, total_words)

        # Create progress bar for current word
        progress = tqdm(
            total=6, desc=f"Creating card {word_index}/{total_words}", unit="step")

        try:
            # Loop until user is satisfied or cancels
            while True:
                progress.set_description(f"Querying LLM for '{word}'")
                response = llm_client.generate_word_info(word, source_language)
                progress.update(1)

                # Get user validation or auto-accept if -y flag is set
                if args.yes:
                    break
                else:
                    user_choice = ui.validate_llm_response(response, word)

                    if user_choice == 'y':
                        break
                    elif user_choice == 'n':
                        ui.show_word_skipped(word)
                        progress.close()
                        break
                    elif user_choice == 'r':
                        print("Restarting query...")
                        progress.n -= 1
                        continue

            # Skip to next word if user cancelled this one
            if not args.yes and user_choice == 'n':
                continue

            # Process response
            progress.set_description("Processing response")
            word_info = card_creator.parse_llm_response(response)
            progress.update(1)

            # Create card with detailed progress
            result = card_creator.create_card_with_progress(
                word, word_info, source_language, progress)

            progress.close()
            ui.show_word_success(word, word_index, total_words)

        except KeyboardInterrupt:
            progress.close()
            ui.show_cancellation()
            sys.exit(0)
        except Exception as e:
            progress.close()
            ui.show_word_error(word, str(e))
            if not ui.ask_continue_on_error():
                sys.exit(1)
            continue

    ui.show_processing_complete(total_words)


if __name__ == "__main__":
    main()
