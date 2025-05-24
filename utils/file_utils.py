"""Utilitaires pour la gestion des fichiers temporaires."""

import os


class FileUtils:
    """Utilities for file management."""

    @staticmethod
    def cleanup_temp_files(files):
        """Clean up temporary files."""
        for temp_file in files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
