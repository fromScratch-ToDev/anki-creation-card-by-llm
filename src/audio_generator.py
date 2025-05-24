"""Audio generation module using XTTS."""

import os
from contextlib import redirect_stderr, redirect_stdout

import torch.serialization
from TTS.api import TTS
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsArgs, XttsAudioConfig

from .config import TTS_MODEL, TTS_SPEAKER


class AudioGenerator:
    """Handles audio generation for words and examples."""

    def __init__(self):
        # Supprimer les avertissements transformers via variable d'environnement
        os.environ["TRANSFORMERS_VERBOSITY"] = "error"
        self._setup_torch_globals()
        self._tts = None

    def _setup_torch_globals(self):
        """Setup torch serialization safe globals."""
        torch.serialization.add_safe_globals([
            XttsConfig,
            XttsAudioConfig,
            BaseDatasetConfig,
            XttsArgs
        ])

    def _get_tts_instance(self):
        """Get or create TTS instance."""
        if self._tts is None:
            with open(os.devnull, 'w') as fnull:
                with redirect_stdout(fnull), redirect_stderr(fnull):
                    self._tts = TTS(
                        model_name=TTS_MODEL,
                        progress_bar=False,
                        gpu=False
                    )
        return self._tts

    def generate_audio(self, text: str, filename: str, language: str):
        """Generate audio file for given text."""
        # Clean text
        if text.lower().startswith("exemple :"):
            text = text[len("exemple :"):].strip()

        tts = self._get_tts_instance()

        # Redirect all outputs to suppress console messages
        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull), redirect_stderr(fnull):
                tts.tts_to_file(
                    text=text,
                    file_path=filename,
                    language=language,
                    speaker=TTS_SPEAKER
                )
