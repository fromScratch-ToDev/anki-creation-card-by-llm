"""Point d'entrée principal"""

import os
import sys

from app.main import main

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    main()
