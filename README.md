# File Explorer Tkinter
## Description

Application graphique développée en Python avec Tkinter permettant d'explorer l'arborescence d'un répertoire et d'afficher des informations sur les fichiers sélectionnés.

L'application propose :

- Affichage récursif de l'arborescence des dossiers et fichiers.
- Visualisation des informations d'un fichier sélectionné.
- Interface graphique simple avec plusieurs panneaux.
- Affichage des informations système du PC (prévu dans la structure du projet).
Fonctionnalités
- Exploration de répertoire
- Sélection d'un dossier grâce à filedialog.askdirectory().
- Parcours récursif des sous-dossiers.
- Affichage dans un widget Treeview.

## Informations sur les fichiers

Pour chaque fichier sélectionné :
- Nom
- Chemin complet
- Type
- Taille
- Date de modification
- Permissions

Les informations sont affichées dans des champs en lecture seule.

## Interface graphique

L'application est organisée en trois sections :

- Directory Tree	Arborescence des dossiers et fichiers
- File Information	Informations détaillées sur le fichier sélectionné
- Information PC	Zone réservée aux informations système

## Technologies utilisées

- Python 3
- Tkinter
- ttk (Treeview)
- pathlib
- os
- datetime
- Pillow (PIL)
- platform

## Installation

1. Cloner le projet
git clone https://github.com/votre-utilisateur/file-explorer.git
cd file-explorer

2. Installer les dépendances
pip install pillow

## Exécution

Lancer le programme :

python fileexplorer.py

## Utilisation

- Ouvrir l'application.
- Dans le menu File, sélectionner Display Directory.
- Choisir un dossier.
- Parcourir l'arborescence affichée.
- Sélectionner un fichier pour consulter ses informations.
- Fonctions principales
- display_directory()

Ouvre un sélecteur de dossiers puis construit l'arborescence du répertoire choisi.

- populate_tree(tree, parent, folder)

Fonction récursive permettant de parcourir tous les sous-dossiers et fichiers.

- display_file_info(event)

Affiche les informations du fichier sélectionné dans les champs dédiés.

- update_entry(entry, value)

Met à jour un champ Entry configuré en lecture seule.

## Auteur

- Emel Keres
- Date : 28/08/2026
- Classe : SI-C3b

## Licence

Projet pédagogique réalisé dans le cadre d'un apprentissage du développement Python et de l'interface graphique Tkinter.
