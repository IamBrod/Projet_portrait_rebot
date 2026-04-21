# Guide d'installation — Portrait Robot

## Présentation

Ce document présente la procédure d'installation complète du projet Portrait Robot. Il s'agit d'une application Python qui repose sur un réseau de neurones de type VAE (Variational AutoEncoder, c'est-à-dire un auto-encodeur variationnel) pour générer et manipuler des visages de manière interactive. On peut alors se demander quelles étapes sont nécessaires pour faire fonctionner un tel système sur une machine personnelle. Ce guide répond à cette question en trois parties : la vérification des prérequis, l'installation des dépendances et le lancement de l'application.

---

## Prérequis

Tout d'abord, avant d'installer quoi que ce soit, il convient de vérifier que votre environnement répond aux exigences minimales du projet.

### Python

Le projet nécessite **Python 3.10 ou une version ultérieure**. Pour vérifier la version installée sur votre machine, ouvrez un terminal et exécutez la commande suivante :

```bash
python --version
```

Si Python n'est pas installé, vous pouvez le télécharger depuis le site officiel : [https://www.python.org/downloads/](https://www.python.org/downloads/). Il est recommandé de cocher l'option *Add Python to PATH* lors de l'installation sur Windows, ce qui permet d'utiliser Python directement depuis n'importe quel terminal sans configuration supplémentaire.

### GPU (facultatif mais recommandé)

Le moteur d'intelligence artificielle peut fonctionner aussi bien sur CPU (le processeur principal de votre machine) que sur GPU (une carte graphique compatible CUDA, c'est-à-dire une carte NVIDIA avec les pilotes appropriés). L'utilisation d'un GPU réduit considérablement le temps de génération des visages. Si aucun GPU compatible n'est détecté, le système bascule automatiquement sur le CPU, ce qui ne nécessite aucune configuration supplémentaire de votre part.

---

## Installation des dépendances

Puis, une fois Python installé, il faut récupérer le code et installer les bibliothèques dont le projet a besoin.

### Étape 1 — Cloner le dépôt

Commencez par télécharger le code source du projet depuis GitHub. Pour cela, ouvrez un terminal dans le dossier où vous souhaitez placer le projet, puis exécutez :

```bash
git clone https://github.com/IamBrod/Projet_portrait_rebot.git
cd Projet_portrait_rebot
```

Si vous ne disposez pas de Git, vous pouvez également télécharger le projet sous forme d'archive ZIP directement depuis la page GitHub du projet, puis extraire le dossier.

### Étape 2 — Créer un environnement virtuel (recommandé)

Il est fortement conseillé de créer un environnement virtuel (c'est-à-dire un espace Python isolé) pour éviter tout conflit entre les bibliothèques de ce projet et celles d'autres projets présents sur votre machine.

```bash
python -m venv venv
```

Puis activez-le selon votre système d'exploitation :

- **Windows :**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux :**
  ```bash
  source venv/bin/activate
  ```

Une fois activé, votre terminal affiche le nom de l'environnement entre parenthèses `(venv)`, ce qui indique que toutes les installations suivantes seront isolées dans cet espace.

### Étape 3 — Installer PyTorch

PyTorch est la bibliothèque centrale du projet. Son installation dépend de votre configuration matérielle.

**Avec GPU (CUDA 11.8) :**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**Sans GPU (CPU uniquement) :**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

Pour connaître la version de CUDA compatible avec votre carte graphique, vous pouvez consulter le configurateur officiel de PyTorch : [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/).

### Étape 4 — Installer les autres dépendances

Les bibliothèques restantes s'installent en une seule commande :

```bash
pip install customtkinter Pillow pandas
```

Voici le rôle de chacune :

- **customtkinter** — bibliothèque d'interface graphique moderne basée sur Tkinter, qui permet d'afficher les boutons, les sélecteurs et les images dans l'application.
- **Pillow (PIL)** — bibliothèque de manipulation d'images, utilisée pour charger, transformer et afficher les portraits générés.
- **pandas** — bibliothèque d'analyse de données, utilisée ici pour lire le fichier d'annotations `1000_attr.txt` qui répertorie les 40 attributs de chaque image de référence.

---

## Téléchargement automatique des poids du modèle

Après avoir vu l'installation des dépendances, il reste un point important à connaître avant de lancer l'application : les **poids du réseau de neurones** (c'est-à-dire les paramètres appris lors de l'entraînement, stockés dans le fichier `weight_ia.pth`) ne sont pas inclus dans le dépôt GitHub en raison de leur taille importante (environ 376 Mo).

Ce téléchargement est entièrement automatisé. Au **premier lancement** de l'application, le moteur vérifie lui-même la présence du fichier `weight_ia.pth` dans le dossier du projet. S'il est absent, il le télécharge automatiquement depuis les *Releases* du dépôt GitHub, puis l'enregistre localement. Les lancements suivants n'effectueront plus ce téléchargement, ce qui explique que le premier démarrage peut prendre quelques minutes selon la vitesse de votre connexion internet.

---

## Lancement de l'application

Enfin, une fois toutes les dépendances installées, lancez l'interface graphique avec la commande suivante, depuis le dossier racine du projet :

```bash
python interface_graphique.py
```

L'application s'ouvre alors et affiche l'interface de génération de portraits robots. Vous pouvez dès lors :

1. **Sélectionner des caractéristiques** dans les menus déroulants (couleur des cheveux, accessoires, type de barbe, etc.).
2. **Générer un suspect initial** en cliquant sur le bouton correspondant, ce qui produit un premier visage à partir de vos critères ou de manière aléatoire.
3. **Explorer des variantes (mutants)** générées automatiquement autour du visage actuel.
4. **Affiner le résultat** en sélectionnant un mutant comme nouvelle base et en recommençant le processus.
5. **Fusionner deux visages** pour créer un morphing progressif entre deux portraits.

---

## Résolution des problèmes courants

| Problème | Cause probable | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'customtkinter'` | Dépendance manquante | Exécutez `pip install customtkinter` |
| `ModuleNotFoundError: No module named 'torch'` | PyTorch non installé | Suivez l'étape 3 de ce guide |
| Le téléchargement des poids échoue | Connexion internet instable | Relancez l'application ou téléchargez manuellement `weight_ia.pth` depuis les Releases GitHub |
| L'interface ne s'affiche pas | Problème avec Tkinter sur Linux | Installez `python3-tk` via `sudo apt install python3-tk` |
| Génération très lente | Aucun GPU détecté | Fonctionnement normal en mode CPU — aucune action requise |

---

## Test du moteur (optionnel)

Si vous souhaitez vérifier que l'ensemble du moteur fonctionne correctement sans passer par l'interface graphique, vous pouvez exécuter le script de test intégré à `moteur_ia.py` :

```bash
python moteur_ia.py
```

Ce script exécute six tests successifs — création d'un suspect, génération de mutants, application de curseurs manuels, morphing total, morphing partiel et évolution génétique sur plusieurs générations — et sauvegarde les images résultantes dans le dossier courant. C'est une façon de s'assurer que l'installation est complète et que le réseau de neurones fonctionne comme prévu avant d'utiliser l'interface.
