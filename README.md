# Portrait Robot — Génération de visages par intelligence artificielle

## Présentation

Ce projet est une application de génération de portraits robots assistée par intelligence artificielle. Plus précisément, il s'agit d'un système interactif qui permet à un utilisateur de construire progressivement un visage à partir de caractéristiques visuelles choisies, à la manière d'un portrait robot utilisé dans les enquêtes criminelles, mais piloté par un réseau de neurones.

On peut alors se demander comment un tel système parvient à produire des visages réalistes et modulables à partir de simples attributs textuels. La réponse repose sur trois composants que l'on va présenter : l'architecture de l'IA, le moteur de génération et l'interface graphique.

---

## Architecture du projet

```
Projet_portrait_rebot/
│
├── architecture_ia.py          # Définition du réseau de neurones (VAE convolutif)
├── moteur_ia.py                # Moteur de génération (encodage, mutation, morphing)
├── interface_graphique.py      # Interface utilisateur (customtkinter)
│
├── tous_les_vecteurs_attributs.pt  # Vecteurs d'attributs pré-calculés
├── 1000_attr.txt               # Fichier d'annotations des 1 000 images de référence
├── 1000_image/                 # Images de visages de référence (base d'encodage)
│
└── weight_ia.pth               # Poids du modèle (téléchargés automatiquement au 1er lancement)
```

---

## Fonctionnement général

Tout d'abord, le cœur du système repose sur un **VAE convolutif** (Variational AutoEncoder, c'est-à-dire un auto-encodeur variationnel), défini dans `architecture_ia.py`. Ce type de réseau de neurones est capable d'apprendre à compresser une image de visage en un vecteur de 1 024 nombres (appelé *espace latent*), puis à reconstruire une image à partir de ce vecteur. C'est cette propriété qui rend possible la manipulation continue des traits d'un visage.

Puis, le **moteur de génération** (`moteur_ia.py`) exploite cet espace latent pour proposer cinq opérations principales :

1. **Créer un suspect initial** — soit à partir d'une image de référence encodée, soit de manière totalement aléatoire en tirant un vecteur latent au hasard.
2. **Générer des mutants** — le moteur produit plusieurs variantes du visage actuel en appliquant des modifications aléatoires contrôlées sur l'espace latent, ce qui crée des propositions légèrement différentes que l'utilisateur peut évaluer.
3. **Appliquer des mutations choisies** — l'utilisateur peut directement orienter un attribut précis (sourire, lunettes, âge, etc.) en déplaçant un curseur dans l'interface. Le moteur traduit ce choix en une modification vectorielle dans l'espace latent.
4. **Fusionner deux visages (morphing total)** — le système calcule une interpolation linéaire entre deux vecteurs latents, produisant une gamme d'images qui vont progressivement d'un visage à l'autre.
5. **Fusion partielle (style mixing)** — une variante du morphing qui ne mélange qu'une portion du vecteur latent, permettant de transférer certains traits d'un visage à l'autre tout en conservant les autres caractéristiques.

Enfin, l'**interface graphique** (`interface_graphique.py`), construite avec la bibliothèque `customtkinter`, expose l'ensemble de ces fonctions à l'utilisateur sous forme de boutons, de sélecteurs et d'affichages d'images. Les attributs sont regroupés en catégories (couleur de cheveux, accessoires, barbe, bouche, yeux, etc.) et chaque sélection est traduite en temps réel en une modification du visage généré.

---

## Les attributs disponibles

Le projet prend en charge **40 attributs faciaux** issus du dataset CelebA, que l'on peut regrouper ainsi :

| Catégorie | Attributs |
|---|---|
| Cheveux | Brun, Blond, Noir, Gris, Ondulé, Raide, Chauve, Frange, Ligne de recul |
| Accessoires | Boucles d'oreilles, Chapeau, Collier, Rouge à lèvres, Cravate, Lunettes |
| Barbe | Moustache, Bouc, Sans barbe, Rouflaquettes, Barbe de 3 jours |
| Bouche | Souriant, Bouche légèrement ouverte, Grosses lèvres |
| Yeux | Yeux étroits, Cernes, Sourcils broussailleux, Sourcils arqués |
| Visage | Visage ovale, Peau pâle, Maquillage, Joues rosées, Pommettes saillantes, Double menton, Joufflu |
| Nez | Grand nez, Nez pointu |
| Âge / Genre | Jeune, Masculin |
| Image | Floue, Nette |

---

## Technologies utilisées

- **Python 3.10+**
- **PyTorch** — entraînement et inférence du réseau de neurones
- **torchvision** — transformations d'images et utilitaires
- **customtkinter** — interface graphique moderne
- **Pillow (PIL)** — manipulation d'images
- **pandas** — lecture du fichier d'annotations

---

## Guide d'installation

Pour installer et lancer le projet sur votre machine, veuillez consulter le fichier dédié :

➡️ **[INSTALLATION.md](./INSTALLATION.md)**

---

## Auteurs

Projet développé dans le cadre d'un cursus en informatique et intelligence artificielle.
