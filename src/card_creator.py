"""Main card creation logic."""

import os
from dataclasses import dataclass
from typing import Tuple

from .anki_client import AnkiClient
from .audio_generator import AudioGenerator
from .config import LANGUAGE_CODES


@dataclass
class WordInfo:
    """Data class for word information."""
    definition: str
    synonyms: str
    example: str


class CardCreator:
    """Main class for creating Anki cards."""

    def __init__(self):
        self.anki_client = AnkiClient()
        self.audio_generator = AudioGenerator()

    def parse_llm_response(self, response: str) -> WordInfo:
        """Parse LLM response into structured data."""
        lines = [line.strip() for line in response.split("\n") if line.strip()]

        return WordInfo(
            definition=lines[0] if len(lines) > 0 else "",
            synonyms=lines[1] if len(lines) > 1 else "",
            example=lines[2] if len(lines) > 2 else ""
        )

    def generate_audio_files(self, word: str, example: str, language_code: str) -> Tuple[str, str]:
        """Generate audio files for word and example."""
        word_audio = f"temp_word_{word}.mp3"
        example_audio = f"temp_example_{word}.mp3"

        self.audio_generator.generate_audio(word, word_audio, language_code)
        self.audio_generator.generate_audio(
            example, example_audio, language_code)

        return word_audio, example_audio

    def create_card(self, word: str, word_info: WordInfo, deck_name: str) -> dict:
        """Create complete Anki card with audio."""
        # Ensure deck exists
        self.anki_client.create_deck_if_not_exists(deck_name)

        # Get language code
        language_code = LANGUAGE_CODES.get(deck_name.lower(), "en")

        # Generate audio files
        word_audio, example_audio = self.generate_audio_files(
            word, word_info.example, language_code
        )

        try:
            # Add media files to Anki
            self.anki_client.add_media_file(f"word_{word}.mp3", word_audio)
            self.anki_client.add_media_file(
                f"example_{word}.mp3", example_audio)

            # Create card content
            front_content = f"{word} [sound:word_{word}.mp3]"
            back_content = f"""{word_info.definition}<br>
                              {word_info.synonyms}<br>
                              {word_info.example} [sound:example_{word}.mp3]"""

            # Add note to Anki
            result = self.anki_client.add_note(
                deck_name, front_content, back_content)

            return result

        finally:
            # Clean up temp files
            for temp_file in [word_audio, example_audio]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)

    def create_card_with_progress(self, word: str, word_info: WordInfo, deck_name: str, progress) -> dict:
        """Create complete Anki card with audio and detailed progress updates."""
        # Ensure deck exists
        progress.set_description("Creating deck")
        self.anki_client.create_deck_if_not_exists(deck_name)
        progress.update(1)

        # Get language code
        language_code = LANGUAGE_CODES.get(deck_name.lower(), "en")

        # Generate word audio
        progress.set_description("Generating word audio")
        word_audio = f"temp_word_{word}.mp3"
        self.audio_generator.generate_audio(word, word_audio, language_code)
        progress.update(1)

        # Generate example audio
        progress.set_description("Generating example audio")
        example_audio = f"temp_example_{word}.mp3"
        self.audio_generator.generate_audio(
            word_info.example, example_audio, language_code)
        progress.update(1)

        try:
            # Add media files to Anki
            progress.set_description("Adding media to Anki")
            self.anki_client.add_media_file(f"word_{word}.mp3", word_audio)
            self.anki_client.add_media_file(
                f"example_{word}.mp3", example_audio)
            progress.update(1)

            # Create and add note
            progress.set_description("Creating Anki card")
            front_content = f"{word} [sound:word_{word}.mp3]"
            back_content = f"""{word_info.definition}<br>
                              {word_info.synonyms}<br>
                              {word_info.example} [sound:example_{word}.mp3]"""

            result = self.anki_client.add_note(
                deck_name, front_content, back_content)
            progress.update(1)

            return result

        finally:
            # Clean up temp files
            for temp_file in [word_audio, example_audio]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
