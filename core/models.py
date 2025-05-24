"""Classes de données pour l'application."""

from dataclasses import dataclass


@dataclass
class WordInfo:
    """Data class for word information."""
    definition: str
    synonyms: str
    example: str
