"""Module pour trouver l'exécutable Anki sur le système."""

import os
import subprocess
import sys


class AnkiFinder:
    """Classe pour localiser l'exécutable Anki sur différents systèmes."""

    @staticmethod
    def find_anki_executable():
        """Find Anki executable on the system."""
        if sys.platform == "win32":
            # Emplacements typiques d'Anki sur Windows
            possible_paths = [
                r"C:\Program Files\Anki\anki.exe",
                r"C:\Program Files (x86)\Anki\anki.exe",
                os.path.expanduser(r"~\AppData\Local\Programs\Anki\anki.exe"),
                os.path.expanduser(
                    r"~\AppData\Local\Programs\Anki\Anki.exe"),  # Majuscule
                os.path.expanduser(
                    r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anki\Anki.lnk"),
                "anki.exe",  # Si dans le PATH
                "anki"       # Si dans le PATH
            ]
        else:
            # Unix/Linux/Mac
            possible_paths = [
                "/usr/bin/anki",
                "/usr/local/bin/anki",
                "/opt/anki/anki",
                "anki"  # Si dans le PATH
            ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
            # Vérifier aussi si la commande est disponible dans le PATH
            try:
                subprocess.run([path, "--version"],
                               capture_output=True, timeout=5)
                return path
            except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
                continue

        return None
