# affichage d'un répertoire dans une fenêtre tkinter
# Emel 28.08.26
# SI-C3b
# hello world

import tkinter as tk
import os
from tkinter import ttk # pour le treeview
from tkinter import filedialog # boite dialogue pour chercher un répertoire
from pathlib import Path # fonctions de répertoire
from datetime import datetime  # pour la date de modification
from PIL import Image, ImageTk # pour importer les images qui sont en jpg, pour le logo de la fenêtre
import platform # pour les infos sur le pc

node_paths = {} #garder les chemins complets

# fonction utilitaire pour remplir les Entry readonly
def update_entry(entry, value):
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, value)
    entry.config(state="readonly")

# afficher les informations du fichier sélectionné
def display_file_info(event):
    selected_nodes = tree.selection()

    if not selected_nodes:
        return

    file_path = node_paths[selected_nodes[0]]
    file_info = file_path.stat()

    # nom
    name = file_path.name

    # chemin
    path = str(file_path.resolve())

    # type
    if file_path.is_dir():
        file_type = "Directory"
    else:
        file_type = file_path.suffix or "No extension"

    # taille en KB
    size_kb = file_info.st_size / 1024
    size = f"{size_kb:.2f} KB"

    # date de modification
    modified = datetime.fromtimestamp(
        file_info.st_mtime
    ).strftime("%d.%m.%Y")

    # permissions
    permissions = []

    if os.access(file_path, os.R_OK):
        permissions.append("Read")

    if os.access(file_path, os.W_OK):
        permissions.append("Write")

    if os.access(file_path, os.X_OK):
        permissions.append("Execute")

    permissions = " / ".join(permissions)

    # mise à jour des champs
    update_entry(entry_name, name)
    update_entry(entry_path, path)
    update_entry(entry_type, file_type)
    update_entry(entry_size, size)
    update_entry(entry_date, modified)
    update_entry(entry_permissions, permissions)

# afficher un répertoire
def display_directory():
    tree.delete(*tree.get_children()) # vider le treeview
    node_paths.clear()
    root_folder = Path(filedialog.askdirectory()) # demander un répertoire

    # insérer le noeud racine (déjà ouvert)
    root_node = tree.insert("","end", text=f"📁 {root_folder.resolve()}",open=True )
    # garder l'info du chemin complet
    node_paths[root_node] = root_folder

    # appeler la recherche des noeuds enfants
    populate_tree(tree, root_node, root_folder)

    # afficher le tableau des node
    for node, path in node_paths.items():
        print(node, ":", path)

# recherche des noeuds enfants (récursif)
def populate_tree(tree, parent, folder):
    # pour tous les noeuds enfants du folder
    for item in folder.iterdir():
        item_name = f"📁 {item.name}" if item.is_dir() else f"🗎 {item.name}"
        node = tree.insert(parent, "end", text=item_name)
        node_paths[node] = item # garder l'info du chemin complet
        if item.is_dir():
            # cas d'un répertoire, rappeler les enfants de l'enfant (peut être long)
            populate_tree(tree,node,item)

# fenêtre principale appelée window
window = tk.Tk()
window.title("file explorer")
window.geometry("800x600")
img = Image.open(r"C:\3eme\ProjDev\sasuke.jpg")
icon = ImageTk.PhotoImage(img)
window.iconphoto(False, icon)
window.configure(bg="white")

# configuration de 2 colonnes dans window, la seconde plus large
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.rowconfigure(0, weight=1) # une ligne (pour le treeview)

# création du menu principal
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="display directory", command=display_directory)
file_menu.add_separator()
file_menu.add_command(label="quit", command=window.destroy)
menu_bar.add_cascade(label="file", menu=file_menu)
menu_bar.add_cascade(label="tools", menu=tk.Menu(menu_bar, tearoff=False))
menu_bar.add_cascade(label="help", menu=tk.Menu(menu_bar, tearoff=False))
window.config(menu=menu_bar)

# frame principal pour contenir les 3 frames
main_frame = tk.Frame(window, bg="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)
main_frame.config(bd=0, bg="white")

# frame pour le treeview 
frame_tree = tk.LabelFrame(main_frame, text="directory tree")
frame_tree.pack(side="left", fill="both", expand=True, padx=5)
frame_tree.config(bd=0, bg="white")

#frame pour les informations sur le fichier
frame_info = tk.LabelFrame(main_frame, text="file information")
frame_info.pack(side="left", fill="both", expand=True, padx=5)
frame_info.config(bd=0, bg="white")

# frame pour les informations sur le pc
frame_pc = tk.LabelFrame(main_frame, text="information pc")
frame_pc.pack(side="left", fill="both", expand=True, padx=5)
frame_pc.config(bd=0, bg="white")

# style du file explorer
style = ttk.Style()

style.configure("Treeview", font=("Arial", 15), rowheight=24)

tree = ttk.Treeview(frame_tree)
tree.heading("#0")

tree.pack(fill="both", expand=True, padx=5, pady=5)
tree.bind("<<TreeviewSelect>>", display_file_info)

# frame avec contour gris pour les informations sur le fichier
content_info = tk.Frame(frame_info, highlightbackground="gray",
highlightthickness=1, bg="white")
content_info.pack(fill="both", expand=True, padx=5, pady=5)

# frame pour les informations sur le fichier
tk.Label(content_info, text="name").pack(pady=(10,0))
entry_name = tk.Entry(content_info, state="readonly")
entry_name.pack(fill="x", padx=10)

tk.Label(content_info, text="path").pack(pady=(10, 0))
entry_path = tk.Entry(content_info, state="readonly")
entry_path.pack(fill="x", padx=10)

tk.Label(content_info, text="type").pack(pady=(10, 0))
entry_type = tk.Entry(content_info, state="readonly")
entry_type.pack(fill="x", padx=10)

tk.Label(content_info, text="size").pack(pady=(10, 0))
entry_size = tk.Entry(content_info, state="readonly")
entry_size.pack(fill="x", padx=10)

tk.Label(content_info, text="modified").pack(pady=(10, 0))
entry_date = tk.Entry(content_info, state="readonly")
entry_date.pack(fill="x", padx=10)

tk.Label(content_info, text="permissions").pack(pady=(10, 0))
entry_permissions = tk.Entry(content_info, state="readonly")
entry_permissions.pack(fill="x", padx=10)

# frame pour les informations sur le pc
content_pc = tk.Frame(frame_pc, highlightbackground="gray", highlightthickness=1, bg="white")
content_pc.pack(fill="both", expand=True, padx=5, pady=5)

# la boucle principale
window.mainloop()