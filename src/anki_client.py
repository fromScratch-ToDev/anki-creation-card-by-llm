"""Anki Connect client for card management."""

import base64
import os
import sys

import requests

from .config import ANKI_CONNECT_URL


class AnkiClient:
    """Handles communication with Anki Connect."""

    def __init__(self):
        self.api_url = ANKI_CONNECT_URL
        self._ensure_anki_running()

    def _is_anki_running(self) -> bool:
        """Check if Anki Connect is available."""
        try:
            response = requests.post(self.api_url, json={
                "action": "version",
                "version": 6
            }, timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _ensure_anki_running(self):
        """Ensure Anki is running, display message if not."""
        if not self._is_anki_running():
            print("⚠️  Anki n'est pas démarré ou Anki Connect n'est pas disponible")
            print("\n📋 Pour utiliser ce programme, veuillez :")
            print("1. Démarrer l'application Anki")
            print("2. Vérifier que le plugin Anki Connect est installé et activé")
            print("3. Relancer ce programme une fois Anki démarré")
            print("\n❌ Le programme va maintenant se fermer.")
            input("\nAppuyez sur Entrée pour fermer...")
            sys.exit(1)

    def create_deck_if_not_exists(self, deck_name: str):
        """Create deck if it doesn't exist."""
        payload = {
            "action": "createDeck",
            "version": 6,
            "params": {"deck": deck_name}
        }
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def add_media_file(self, filename: str, file_path: str):
        """Add media file to Anki."""
        with open(file_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')

        payload = {
            "action": "storeMediaFile",
            "version": 6,
            "params": {
                "filename": filename,
                "data": data
            }
        }
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json()

    def add_note(self, deck_name: str, front_content: str, back_content: str):
        """Add note to Anki deck."""
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front_content,
                        "Back": back_content
                    },
                    "options": {"allowDuplicate": False},
                    "tags": ["auto-llm", deck_name.lower()]
                }
            }
        }
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json()
