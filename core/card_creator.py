"""Logique principale de création de cartes Anki."""

from config.languages import LANGUAGE_CODES
from services.anki.client import AnkiClient
from services.audio.tts_generator import TTSGenerator
from utils.file_utils import FileUtils

from .models import WordInfo
from .word_processor import WordProcessor


class CardCreator:
    """Main class for creating Anki cards."""

    def __init__(self, progress=None):
        self.progress = progress
        if progress:
            progress.set_description("Connecting to Anki")
        self.anki_client = AnkiClient(progress)
        self.audio_generator = TTSGenerator()
        if progress:
            progress.update(1)

    def create_card_with_progress(self, word: str, word_info: WordInfo, deck_name: str, progress) -> dict:
        """Create complete Anki card with audio and detailed progress updates."""
        self._ensure_deck_exists(deck_name, progress)
        language_code = self._get_language_code(deck_name)

        word_audio = self._generate_audio_with_progress(
            text=word,
            filename=f"temp_word_{word}.mp3",
            language_code=language_code,
            progress=progress,
            description="Generating word audio"
        )

        example_text = WordProcessor.clean_example_text(word_info.example)
        example_audio = self._generate_audio_with_progress(
            text=example_text,
            filename=f"temp_example_{word}.mp3",
            language_code=language_code,
            progress=progress,
            description="Generating example audio"
        )

        try:
            self._add_media_files_with_progress(
                word, word_audio, example_audio, progress)
            result = self._create_anki_note_with_progress(
                word, word_info, deck_name, language_code, progress)
            return result
        finally:
            FileUtils.cleanup_temp_files([word_audio, example_audio])

    def _ensure_deck_exists(self, deck_name: str, progress):
        progress.set_description("Creating deck")
        self.anki_client.create_deck_if_not_exists(deck_name)
        progress.update(1)

    def _get_language_code(self, deck_name: str) -> str:
        return LANGUAGE_CODES.get(deck_name.lower(), "en")

    def _generate_audio_with_progress(self, text: str, filename: str, language_code: str, progress, description: str) -> str:
        progress.set_description(description)
        self.audio_generator.generate_audio(text, filename, language_code)
        progress.update(1)
        return filename

    def _add_media_files_with_progress(self, word: str, word_audio: str, example_audio: str, progress):
        progress.set_description("Adding media to Anki")
        self.anki_client.add_media_file(f"word_{word}.mp3", word_audio)
        self.anki_client.add_media_file(f"example_{word}.mp3", example_audio)
        progress.update(1)

    def _create_anki_note_with_progress(self, word: str, word_info: WordInfo, deck_name: str, language_code: str, progress) -> dict:
        progress.set_description("Creating Anki card")

        if language_code == "en":
            front_content = f"{word} [sound:word_{word}.mp3]"
        else:
            front_content = word

        back_content = (
            f"{word_info.definition}<br>"
            f"{word_info.synonyms}<br>"
            f"{word_info.example} [sound:example_{word}.mp3]"
        )
        result = self.anki_client.add_note(
            deck_name, front_content, back_content)
        progress.update(1)
        return result
