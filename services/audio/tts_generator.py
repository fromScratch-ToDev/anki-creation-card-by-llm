"""Générateur audio utilisant des modèles TTS légers spécifiques aux langues."""

import os
from contextlib import redirect_stderr, redirect_stdout

from TTS.api import TTS

from config.languages import DEFAULT_TTS_MODEL, TTS_MODELS


class TTSGenerator:
    """Handles audio generation for words and examples using lightweight TTS models."""

    def __init__(self):
        self._tts_instances = {}

    def _get_tts_model_for_language(self, language_code: str) -> str:
        """Get the appropriate lightweight TTS model for the given language."""
        return TTS_MODELS.get(language_code, DEFAULT_TTS_MODEL)

    def _get_tts_instance(self, language_code: str):
        """Get or create TTS instance for specific language."""
        if language_code not in self._tts_instances:
            model_name = self._get_tts_model_for_language(language_code)
            # Créer l'instance TTS en supprimant les logs d'initialisation
            with open(os.devnull, 'w') as fnull:
                # Rediriger uniquement stdout, pas stderr pour voir la progression
                with redirect_stdout(fnull):

                    self._tts_instances[language_code] = TTS(
                        model_name=model_name,
                        progress_bar=True,
                        gpu=False
                    )

        return self._tts_instances[language_code]

    def generate_audio(self, text: str, filename: str, language: str):
        """Generate audio file for given text using monolanguage model."""

        # Get TTS instance for this language
        tts = self._get_tts_instance(language)

        # Generate audio with suppressed output
        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull), redirect_stderr(fnull):
                tts.tts_to_file(
                    text=text,
                    file_path=filename
                )
