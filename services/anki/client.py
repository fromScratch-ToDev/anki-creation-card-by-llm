"""Client Anki Connect pour la gestion des cartes."""

import base64
import time

import requests

from config.settings import ANKI_CONNECT_URL

from .launcher import AnkiLauncher


class AnkiClient:
    """Handles communication with Anki Connect."""

    def __init__(self, progress=None):
        self.api_url = ANKI_CONNECT_URL
        self.progress = progress
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
        """Ensure Anki is running, start it if necessary, and wait for server."""
        # Vérifier d'abord si Anki est déjà en cours d'exécution
        if self._is_anki_running():
            if not self.progress:
                print("✅ Anki server is already available")
            return

        # Démarrer Anki s'il n'est pas en cours d'exécution
        AnkiLauncher.start_anki_silent(self.progress)

        # Attendre que le serveur soit disponible
        self._wait_for_anki_server()

    def _wait_for_anki_server(self):
        """Wait for Anki server to become available."""
        if self.progress:
            self.progress.set_description("Waiting for Anki server...")
        else:
            print("⏳ Waiting for Anki server to be available...")

        max_attempts = 30  # Maximum 60 secondes d'attente
        attempts = 0

        while not self._is_anki_running() and attempts < max_attempts:
            if not self.progress:
                print(
                    f"⏳ Anki server not available, waiting... (attempt {attempts + 1}/{max_attempts})")
            time.sleep(2)
            attempts += 1

        if attempts >= max_attempts:
            error_msg = "❌ Timeout: Anki server did not become available within 60 seconds"
            if self.progress:
                self.progress.set_description(error_msg)
            else:
                print(error_msg)
            raise RuntimeError("Anki server startup timeout")

        if not self.progress:
            print("✅ Anki server is available")

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
