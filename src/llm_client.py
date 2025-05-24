"""LLM client for generating word definitions and examples."""

import requests

from .config import OLLAMA_API_URL, OLLAMA_MODEL


class LLMClient:
    """Handles communication with Ollama LLM."""

    def __init__(self, model: str = OLLAMA_MODEL):
        self.model = model
        self.api_url = OLLAMA_API_URL

    def generate_word_info(self, word: str, language: str) -> str:
        """Generate definition, synonyms and example for a word."""
        prompt = f"""
        Donne-moi des infos sur le mot {language.lower()} « {word} » :

        - Définition en français (courte phrase)
        - Synonymes en {language.lower()}
        - Exemple en {language.lower()}

        Supprime tout ce qui est entre parenthèses. Répond exactement dans ce format :

        Définition : …  
        Synonymes : …  
        Exemple : …
        """

        return self._ask_ollama(prompt)

    def _ask_ollama(self, prompt: str) -> str:
        """Send request to Ollama API."""
        response = requests.post(self.api_url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        return response.json()["response"]
