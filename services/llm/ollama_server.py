"""Module pour gérer le serveur Ollama."""

import subprocess
import sys
import time

import requests

from config.settings import OLLAMA_API_URL


class OllamaServer:
    """Classe pour gérer le serveur Ollama."""

    @staticmethod
    def is_server_running() -> bool:
        """Vérifier si le serveur Ollama est en cours d'exécution."""
        try:
            response = requests.get(
                f"{OLLAMA_API_URL.replace('/api/generate', '')}/api/tags", timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def start_server(progress=None):
        """Démarrer le serveur Ollama si nécessaire."""
        if OllamaServer.is_server_running():
            if not progress:
                print("✅ Ollama server is already running")
            return

        try:
            if progress:
                progress.set_description("Starting Ollama server...")
            else:
                print("🚀 Starting Ollama server...")

            # Démarrer Ollama en arrière-plan
            if sys.platform == "win32":
                # Sur Windows, utiliser start pour démarrer en arrière-plan
                subprocess.Popen(
                    ["ollama", "serve"],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=False
                )
            else:
                # Sur Unix/Linux/Mac
                subprocess.Popen(
                    ["ollama", "serve"],
                    start_new_session=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    close_fds=Truee
                )

            # Attendre que le serveur soit disponible
            OllamaServer._wait_for_server(progress)

        except FileNotFoundError:
            error_msg = """❌ Ollama executable not found.
Please ensure Ollama is installed and available in your PATH.
Download from: https://ollama.ai/"""
            if progress:
                progress.set_description("Ollama not found")
            else:
                print(error_msg)
            raise RuntimeError("Ollama executable not found")
        except Exception as e:
            error_msg = f"❌ Failed to start Ollama server: {str(e)}"
            if progress:
                progress.set_description(error_msg)
            else:
                print(error_msg)
            raise RuntimeError(f"Failed to start Ollama server: {str(e)}")

    @staticmethod
    def _wait_for_server(progress=None):
        """Attendre que le serveur Ollama soit disponible."""
        if progress:
            progress.set_description("Waiting for Ollama server...")
        else:
            print("⏳ Waiting for Ollama server to be available...")

        max_attempts = 30  # Maximum 60 secondes d'attente
        attempts = 0

        while not OllamaServer.is_server_running() and attempts < max_attempts:
            if not progress:
                print(
                    f"⏳ Ollama server not available, waiting... (attempt {attempts + 1}/{max_attempts})")
            time.sleep(2)
            attempts += 1

        if attempts >= max_attempts:
            error_msg = "❌ Timeout: Ollama server did not become available within 60 seconds"
            if progress:
                progress.set_description(error_msg)
            else:
                print(error_msg)
            raise RuntimeError("Ollama server startup timeout")

        if not progress:
            print("✅ Ollama server is available")

    @staticmethod
    def ensure_server_running(progress=None):
        """S'assurer que le serveur Ollama est en cours d'exécution."""
        if not OllamaServer.is_server_running():
            OllamaServer.start_server(progress)
