"""Configuration principale de l'application."""

# API endpoints
OLLAMA_API_URL = "http://localhost:11434/api/generate"
ANKI_CONNECT_URL = "http://localhost:8765"

# Models
OLLAMA_MODEL = "gemma3:12b"
# Modèle plus léger pour systèmes avec moins de VRAM
OLLAMA_MODEL_LITE = "gemma3:4b"
