"""Point d'entrée principal de l'application."""

import sys

from tqdm import tqdm

from config.languages import LANGUAGES
from config.settings import OLLAMA_MODEL, OLLAMA_MODEL_LITE
from core.card_creator import CardCreator
from core.word_processor import WordProcessor
from services.llm.ollama_client import OllamaClient
from ui.console import ConsoleUI

from .cli import parse_arguments


def main():
    """Main application logic."""
    args = parse_arguments()
    ui = ConsoleUI()

    # Validate input
    if not args.words:
        ui.show_available_languages(LANGUAGES)
        sys.exit(1)

    # Parse multiple words separated by semicolons
    words_list = [word.strip() for word in args.words.split(';')]
    source_language = args.language.capitalize()

    # Select model based on --lite flag
    model = OLLAMA_MODEL_LITE if args.lite else OLLAMA_MODEL

    # Process each word
    total_words = len(words_list)
    ui.show_processing_start(total_words)

    for word_index, word in enumerate(words_list, 1):
        if not word:  # Skip empty strings
            continue

        ui.show_word_progress(word, word_index, total_words)

        # Create progress bar for current word (7 steps now: initialization + anki + 5 existing)
        progress = tqdm(
            total=7, desc=f"Creating card {word_index}/{total_words}", unit="step")

        try:
            # Step 1: Initialization
            progress.set_description("Initializing components")
            # Initialize components here for each word to ensure fresh state
            llm_client = OllamaClient(model=model)
            # Pass progress to handle Anki startup
            card_creator = CardCreator(progress)
            progress.update(1)

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
            word_info = WordProcessor.parse_llm_response(response)
            progress.update(1)

            # Create card with detailed progress
            card_creator.create_card_with_progress(
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
