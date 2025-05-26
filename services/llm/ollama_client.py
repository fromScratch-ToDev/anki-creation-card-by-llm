"""Client LLM pour générer les définitions et exemples de mots."""

import requests

from config.settings import OLLAMA_API_URL, OLLAMA_MODEL

from .ollama_server import OllamaServer


class OllamaClient:
    """Handles communication with Ollama LLM."""

    def __init__(self, model: str = OLLAMA_MODEL, progress=None):
        self.model = model
        self.api_url = OLLAMA_API_URL
        # S'assurer que le serveur Ollama est en cours d'exécution
        OllamaServer.ensure_server_running(progress)

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
        try:
            response = requests.post(self.api_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.ConnectionError:
            # Si la connexion échoue, essayer de redémarrer le serveur
            print("⚠️ Connection to Ollama server lost, attempting to restart...")
            OllamaServer.ensure_server_running()
            # Réessayer la requête
            response = requests.post(self.api_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()
            return response.json()["response"]
