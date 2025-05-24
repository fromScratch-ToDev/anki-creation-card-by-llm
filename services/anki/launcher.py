"""Module pour lancer Anki en mode silencieux."""

import os
import subprocess
import sys

from .finder import AnkiFinder


class AnkiLauncher:
    """Classe pour démarrer Anki en arrière-plan sans logs."""

    @staticmethod
    def start_anki_silent(progress=None):
        """Start Anki process in background if not already running."""
        try:
            if progress:
                progress.set_description("Starting Anki...")
            else:
                print("🚀 Starting Anki in background...")

            # Trouver l'exécutable Anki
            anki_path = AnkiFinder.find_anki_executable()
            if not anki_path:
                raise FileNotFoundError(
                    "Anki executable not found in common locations")

            # Sur Windows, utiliser le script batch pour un démarrage complètement silencieux
            if sys.platform == "win32":
                # Utiliser le script batch pour supprimer tous les logs
                script_dir = os.path.dirname(os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))))
                batch_script = os.path.join(
                    script_dir, "scripts", "start_anki_silent.bat")

                subprocess.Popen(
                    [batch_script, anki_path],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True
                )
            else:
                # Sur Unix/Linux/Mac
                subprocess.Popen(
                    [anki_path],
                    start_new_session=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    close_fds=True
                )

            if not progress:
                print(f"✅ Anki started successfully (silent mode)")

        except FileNotFoundError:
            error_msg = """❌ Anki executable not found. 
Searched in:
- C:\\Program Files\\Anki\\anki.exe
- C:\\Program Files (x86)\\Anki\\anki.exe
- %USERPROFILE%\\AppData\\Local\\Programs\\Anki\\anki.exe
- PATH environment variable

Please ensure Anki is installed or add it to your PATH."""
            if progress:
                progress.set_description("Anki not found")
            else:
                print(error_msg)
            raise RuntimeError("Anki executable not found")
        except Exception as e:
            error_msg = f"❌ Failed to start Anki: {str(e)}"
            if progress:
                progress.set_description(error_msg)
            else:
                print(error_msg)
            raise RuntimeError(f"Failed to start Anki: {str(e)}")
