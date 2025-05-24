"""Configuration des langues et modèles TTS."""

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

# Modèles TTS monolangues de haute qualité (meilleurs modèles disponibles par langue)
TTS_MODELS = {
    "en": "tts_models/en/ljspeech/vits",
    "es": "tts_models/es/css10/vits",
    "fr": "tts_models/fr/css10/vits",
    "ru": "tts_models/ru/ruslan/tacotron2-DDC_ph",
    "pt": "tts_models/pt/cv/vits",
    "ar": "tts_models/ar/cv/vits",
    "zh-cn": "tts_models/zh-CN/baker/tacotron2-DDC-GST",
    "hi": "tts_models/hi/male/glow-tts",
    "bn": "tts_models/bn/male/multi_dataset_male_glow_tts",
    "id": "tts_models/id/male/glow-tts"
}

# Modèle par défaut haute qualité si la langue n'est pas supportée
DEFAULT_TTS_MODEL = "tts_models/en/ljspeech/vits"
