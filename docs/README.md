# Anki Card Creator avec LLM

Un outil automatisé pour créer des cartes Anki avec définitions, synonymes et exemples audio pour l'apprentissage de langues étrangères.

## Fonctionnalités

- ✨ Génération automatique de définitions, synonymes et exemples via LLM (Ollama)
- 🔊 Synthèse vocale de haute qualité pour les mots et exemples
- 🎯 Support de 10 langues principales
- 📚 Création automatique de decks Anki
- 🔄 Traitement par lots de plusieurs mots
- 💾 Modèle LLM léger pour systèmes avec moins de VRAM

## Prérequis

1. **Anki** avec le plugin **AnkiConnect** installé et activé
2. **Ollama** installé avec les modèles :
   - `gemma3:12b` (modèle par défaut, haute qualité)
   - `gemma3:4b` (modèle léger, option `--lite`)
3. **Python 3.10+** avec les dépendances installées

## Installation

```bash
# Cloner le projet
git clone <repository-url>
cd anki-creation-card-by-llm

# Installer les dépendances Python
pip install -r requirements.txt

# Télécharger les modèles Ollama
ollama pull gemma3:12b     # Modèle standard (recommandé)
ollama pull gemma3:4b      # Modèle léger (pour --lite)
```

## Utilisation

### Syntaxe de base

```bash
python anki-create.py "mot(s)" [langue] [options]
```

### Options disponibles

- `-y, --yes` : Accepte automatiquement les réponses du LLM sans confirmation
- `--lite` : Utilise le modèle LLM léger `gemma3:4b` au lieu de `gemma3:12b`
- `--help` : Affiche l'aide complète

### Exemples d'utilisation

#### Mot unique
```bash
# Mot anglais (langue par défaut)
python anki-create.py "hello"

# Mot dans une autre langue
python anki-create.py "hola" "espagnol"
python anki-create.py "こんにちは" "japonais"
```

#### Mots multiples
```bash
# Plusieurs mots séparés par des points-virgules
python anki-create.py "hello; goodbye; you nail it!" "anglais"
```

#### Mode automatique
```bash
# Accepter automatiquement toutes les réponses
python anki-create.py "hello; world" -y
```

#### Mode léger (moins de VRAM)
```bash
# Utiliser le modèle 4B au lieu du 12B
python anki-create.py "hello" --lite
python anki-create.py "hello; world" --lite -y
```

### Langues supportées

| Code | Langue | Deck Anki |
|------|--------|-----------|
| en | Anglais | Anglais |
| es | Espagnol | Espagnol |
| fr | Français | Français |
| zh-cn | Chinois | Chinois |
| ru | Russe | Russe |
| pt | Portugais | Portugais |
| ar | Arabe | Arabe |
| hi | Hindi | Hindi |
| bn | Bengali | Bengali |
| id | Indonésien | Indonésien |

## Choix du modèle LLM

### Modèle standard (gemma3:12b)
- **Avantages** : Qualité supérieure des définitions et exemples
- **Inconvénients** : Nécessite ~8-12 GB de VRAM
- **Recommandé pour** : Systèmes avec GPU puissant

### Modèle léger (gemma3:4b) - Option `--lite`
- **Avantages** : Consommation mémoire réduite (~3-5 GB VRAM), plus rapide
- **Inconvénients** : Qualité légèrement inférieure
- **Recommandé pour** : Systèmes avec GPU limité ou CPU uniquement

## Structure des cartes créées

Chaque carte Anki contient :

**Recto :**
- Le mot étranger
- Audio de prononciation (seulement pour l'anglais)

**Verso :**
- Définition en français
- Synonymes dans la langue originale
- Exemple d'utilisation avec audio

## Dépannage

### Anki ne démarre pas automatiquement
1. Démarrez Anki manuellement
2. Vérifiez qu'AnkiConnect est installé et activé
3. Relancez l'outil

### Erreur de modèle Ollama
```bash
# Vérifier les modèles installés
ollama list

# Installer le modèle manquant
ollama pull gemma3:12b  # ou gemma3:4b pour --lite
```

### Problèmes de VRAM
- Utilisez l'option `--lite` pour réduire l'utilisation mémoire
- Fermez les autres applications utilisant le GPU
- Considérez l'utilisation du CPU uniquement (plus lent)

## Scripts de lancement

### Windows
```bat
# Utiliser anki-create.bat
anki-create.bat "hello" --lite
```

### PowerShell
```powershell
# Utiliser anki-create.ps1
.\anki-create.ps1 "hello" --lite
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Ajouter le support de nouvelles langues
- Améliorer la documentation