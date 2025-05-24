"""Gestion des arguments de ligne de commande."""

import argparse


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Crée des cartes Anki avec définition, synonymes et exemples audio pour des mots étrangers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Exemples d'utilisation:
            python -m app.main "hello"                           # Crée une carte pour le mot anglais "hello"
            python -m app.main "hello; goodbye; you nail it!"    # Crée plusieurs cartes à la fois
            python -m app.main "hola" "espagnol"                 # Crée une carte pour le mot espagnol "hola"
            python -m app.main "こんにちは" "japonais"              # Crée une carte pour le mot japonais "こんにちは"
            python -m app.main "hello; goodbye" -y               # Accepte automatiquement la réponse du LLM
            python -m app.main "hello" --lite                    # Utilise le modèle LLM léger (gemma3:4b)
        """)

    parser.add_argument(
        "words", nargs="?", help="Le(s) mot(s) étranger(s) pour lesquel(s) créer une carte Anki (séparés par des points-virgules)")
    parser.add_argument("language", nargs="?", default="Anglais",
                        help="La langue du mot fourni et nom du deck Anki (défaut: Anglais)")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="Accepte automatiquement la réponse du LLM sans demander confirmation")
    parser.add_argument("--lite", action="store_true",
                        help="Utilise le modèle LLM léger gemma3:4b au lieu de gemma3:12b (recommandé pour les systèmes avec moins de VRAM)")

    return parser.parse_args()
