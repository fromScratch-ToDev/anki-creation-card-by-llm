"""User interface and interaction module."""

import sys
from typing import Literal


class UserInterface:
    """Handles user interactions and validation."""

    @staticmethod
    def validate_llm_response(response: str, word: str) -> Literal['y', 'n', 'r']:
        """Display LLM response and get user confirmation."""
        print(f"\n=== LLM Response for word '{word}' ===")
        print(response)
        print("\n=== Options ===")
        print("y - Accept and create Anki card")
        print("n - Cancel operation")
        print("r - Restart query with the same word")

        while True:
            choice = input("Your choice (y/n/r): ").strip().lower()
            if choice in ['y', 'n', 'r']:
                return choice
            print("Invalid option. Please choose y, n, or r.")

    @staticmethod
    def show_available_languages(languages: dict):
        """Display available languages."""
        print("Veuillez spécifier un mot. Utilisez --help pour plus d'information.")
        print("\nLangues disponibles:")
        for code, name in languages.items():
            print(f"  - {name} ({code})")

    @staticmethod
    def show_processing_start(total_words: int):
        """Show start of processing multiple words."""
        if total_words > 1:
            print(f"\n🚀 Traitement de {total_words} mots/expressions...")

    @staticmethod
    def show_word_progress(word: str, current: int, total: int):
        """Show progress for current word."""
        if total > 1:
            print(f"\n[{current}/{total}] Traitement de: '{word}'")

    @staticmethod
    def show_word_success(word: str, current: int, total: int):
        """Show success for a single word."""
        if total > 1:
            print(f"✅ [{current}/{total}] Carte créée pour '{word}'")
        else:
            print(f"✅ Carte ajoutée pour le mot '{word}'")

    @staticmethod
    def show_word_skipped(word: str):
        """Show that a word was skipped."""
        print(f"⏭️  Mot '{word}' ignoré")

    @staticmethod
    def show_word_error(word: str, error: str):
        """Show error for a specific word."""
        print(f"❌ Erreur pour le mot '{word}': {error}")

    @staticmethod
    def show_processing_complete(total_words: int):
        """Show completion message."""
        if total_words > 1:
            print(
                f"\n🎉 Traitement terminé pour {total_words} mots/expressions!")

    @staticmethod
    def ask_continue_on_error() -> bool:
        """Ask user if they want to continue after an error."""
        while True:
            choice = input(
                "Continuer avec les autres mots? (y/n): ").strip().lower()
            if choice in ['y', 'yes', 'o', 'oui']:
                return True
            elif choice in ['n', 'no', 'non']:
                return False
            print("Répondez par 'y' (oui) ou 'n' (non)")

    @staticmethod
    def show_success(word: str, result: dict):
        """Show success message (legacy method)."""
        print(f"✅ Carte ajoutée pour le mot '{word}' :", result)

    @staticmethod
    def show_cancellation():
        """Show cancellation message."""
        print("Operation cancelled by user.")

    @staticmethod
    def show_anki_connection_status():
        """Show Anki connection status messages."""
        print("🔗 Vérification de la connexion à Anki...")
