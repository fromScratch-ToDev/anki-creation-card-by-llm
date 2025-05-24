"""Configuration constants and language mappings."""

# Dictionnaire des langues les plus parlées avec leurs codes ISO 639-1
LANGUAGES = {
    "en": "Anglais",
    "zh-cn": "Chinois",
    "hi": "Hindi",
    "es": "Espagnol",
    "fr": "Français",
    "ar": "Arabe",
    "bn": "Bengali",
    "ru": "Russe",
    "pt": "Portugais",
    "id": "Indonésien"
}

# Dictionnaire inversé pour recherche par nom de langue
LANGUAGE_CODES = {v.lower(): k for k, v in LANGUAGES.items()}

# API endpoints
OLLAMA_API_URL = "http://localhost:11434/api/generate"
ANKI_CONNECT_URL = "http://localhost:8765"

# Models
OLLAMA_MODEL = "gemma3:12b"
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
TTS_SPEAKER = "Claribel Dervla"
