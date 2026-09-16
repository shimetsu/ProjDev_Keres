# File Explorer Tkinter

## Description

Application graphique développée en Python avec Tkinter permettant d'explorer l'arborescence d'un répertoire et d'afficher des informations détaillées sur les fichiers sélectionnés ainsi que les informations système du PC.

L'application propose :

- Affichage récursif de l'arborescence des dossiers et fichiers avec icônes.
- Visualisation des informations détaillées d'un fichier sélectionné.
- Affichage des informations système du PC en temps réel (processeur, système d'exploitation).
- Interface graphique organisée en trois panneaux principaux.
- Mise à jour automatique des données CPU.

## Fonctionnalités

### Exploration de répertoire
- Sélection d'un dossier grâce à `filedialog.askdirectory()`.
- Parcours récursif des sous-dossiers et fichiers.
- Affichage hiérarchique dans un widget `Treeview`.
- Icônes émojis pour différencier les dossiers (📁) et fichiers (🗎).

### Informations sur les fichiers

Pour chaque fichier ou dossier sélectionné, l'application affiche :
- **Nom** : Nom du fichier/dossier
- **Chemin complet** : Chemin résolu du fichier
- **Type** : Extension du fichier ou "Directory" pour les dossiers
- **Taille** : Taille en KB avec 2 décimales
- **Date de modification** : Format JJ.MM.AAAA
- **Permissions** : Droits d'accès (Read/Write/Execute)

### Informations Processeur (mise à jour en temps réel)
- **Vitesse** : Fréquence CPU en GHz
- **Temps de fonctionnement** : Uptime du PC au format HH:MM:SS
- **Utilisation** : Pourcentage d'utilisation CPU

### Informations Système d'exploitation
- **Édition** : Édition de Windows (ex: Windows 11 Pro)
- **Version** : Numéro de version
- **Date d'installation** : Date d'installation du système

## Interface graphique

L'application est organisée en trois sections principales :

| Section | Contenu |
|---------|---------|
| **Directory Tree** | Arborescence des dossiers et fichiers du répertoire sélectionné |
| **File Information** | Informations détaillées sur le fichier/dossier sélectionné |
| **Information PC** | Informations système en temps réel (processeur et OS) |

## Technologies utilisées

- **Python 3** : Langage de programmation
- **Tkinter** : Framework GUI pour l'interface graphique
- **ttk** : Widgets thématisés (Treeview)
- **pathlib** : Manipulation des chemins de fichiers
- **os** : Vérification des permissions
- **datetime** : Gestion des dates et heures
- **Pillow (PIL)** : Gestion des images
- **platform** : Informations système
- **psutil** : Informations CPU et uptime
- **winreg** : Accès aux registres Windows pour les infos OS

## Installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/shimetsu/ProjDev_Keres.git
   cd ProjDev_Keres
   ```

2. **Installer les dépendances**
   ```bash
   pip install pillow psutil
   ```

3. **Préparer l'icône** (optionnel)
   - Placer un fichier `sasuke.jpg` dans le répertoire du projet pour utiliser comme icône de la fenêtre

## Exécution

Lancer le programme :

```bash
python fileexplorer.py
```

## Utilisation

1. **Ouvrir l'application** : Le programme se lance avec l'interface vierge.
2. **Sélectionner un répertoire** : Cliquer sur le menu `file` → `display directory`.
3. **Choisir un dossier** : Une boîte de dialogue apparaît pour sélectionner le dossier.
4. **Parcourir l'arborescence** : L'arborescence du répertoire sélectionné s'affiche dans le panneau de gauche.
5. **Sélectionner un fichier** : Cliquer sur un fichier ou dossier pour voir ses détails dans le panneau du milieu.
6. **Consulter les infos système** : Le panneau de droite affiche les informations du processeur et du système d'exploitation en temps réel.

## Fonctions principales

### `display_directory()`
Ouvre un sélecteur de dossiers et construit l'arborescence du répertoire choisi. Réinitialise le `Treeview` et le dictionnaire des chemins.

### `populate_tree(tree, parent, folder)`
Fonction récursive parcourant tous les sous-dossiers et fichiers du dossier fourni. Ajoute des nœuds au `Treeview` avec icônes.

### `display_file_info(event)`
Affiche les informations du fichier/dossier sélectionné dans les champs dédiés du panneau File Information.

### `update_entry(entry, value)`
Fonction utilitaire mettant à jour un champ `Entry` configuré en lecture seule.

### `get_cpu_info()`
Récupère les informations du processeur (vitesse, uptime, utilisation) via `psutil`.

### `get_os_info()`
Récupère les informations du système d'exploitation (édition, version, date d'installation) via les registres Windows.

### `refresh_cpu_info()`
Met à jour automatiquement les informations CPU toutes les 1000ms (1 seconde).

## Auteur

- **Nom** : Emel Keres
- **Date** : 16.09.2026
- **Classe** : SI-C3b

## Licence

Projet pédagogique réalisé dans le cadre d'un apprentissage du développement Python et de l'interface graphique Tkinter.
