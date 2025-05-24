"""Module de traitement des mots et des réponses LLM."""

from .models import WordInfo


class WordProcessor:
    """Classe pour traiter les réponses LLM et extraire les informations des mots."""

    @staticmethod
    def parse_llm_response(response: str) -> WordInfo:
        """Parse LLM response into structured data."""
        lines = [line.strip() for line in response.split("\n") if line.strip()]

        return WordInfo(
            definition=lines[0] if len(lines) > 0 else "",
            synonyms=lines[1] if len(lines) > 1 else "",
            example=lines[2] if len(lines) > 2 else ""
        )

    @staticmethod
    def clean_example_text(example: str) -> str:
        """Clean example text by removing 'exemple :' prefix."""
        prefix = "exemple :"
        if example.lower().startswith(prefix):
            return example[len(prefix):].strip()
        return example.strip()
