"""

Name : fileexplorer.py

Author : Emel Keres

Date : 16.09.2026

Purpose : Projet File Explorer Tkinter

"""

import tkinter as tk # pour l'interface graphique
import os # pour les permissions
from tkinter import ttk # pour le treeview
from tkinter import filedialog # boite dialogue pour chercher un répertoire
from pathlib import Path # fonctions de répertoire
from datetime import datetime  # pour la date de modification
from PIL import Image, ImageTk # pour importer les images qui sont en jpg, pour le logo de la fenêtre
import platform # pour les infos sur le pc
import psutil # pour les infos sur le pc (CPU et le temps de fonctionnement)
import winreg # pour les registres Windows

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
    root_node = tree.insert("", "end", text=f"📁 {root_folder.name}", open=True)
    # garder l'info du chemin complet
    node_paths[root_node] = root_folder

    # appeler la recherche des noeuds enfants
    populate_tree(tree, root_node, root_folder)

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

# informations CPU
def get_cpu_info():
    try:
        freq = psutil.cpu_freq()
        if freq:
            speed = f"{freq.current / 1000:.2f} GHz"
        else:
            speed = "Unknown"

        # temps depuis le démarrage du PC
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        total_seconds = int(uptime.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        uptime_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        usage = f"{psutil.cpu_percent(interval=None):.1f} %"
        return speed, uptime_str, usage
    except Exception:
        return "Unknown", "Unknown", "Unknown"

# informations Windows
def get_os_info():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        )
        edition = winreg.QueryValueEx(key, "ProductName")[0]
        try:
            version = winreg.QueryValueEx(key, "DisplayVersion")[0]
        except:
            version = "Unknown"
        install_timestamp = winreg.QueryValueEx(
            key,
            "InstallDate"
        )[0]
        install_date = datetime.fromtimestamp(
            install_timestamp
        ).strftime("%d.%m.%Y")
        return edition, version, install_date
    except Exception:
        return "Unknown", "Unknown", "Unknown"

# mise à jour automatique des informations CPU
def refresh_cpu_info():
    speed, uptime, usage = get_cpu_info()
    lbl_speed.config(text=speed)
    lbl_uptime.config(text=uptime)
    lbl_usage.config(text=usage)
    window.after(1000, refresh_cpu_info)

# fenêtre principale appelée window
# aide de l'ia pour centrer les objets dans la fenetre 
window = tk.Tk()
window.title("file explorer")
window.geometry("1200x650")
img = Image.open(r"sasuke.jpg")
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
frame_pc.pack(side="left", fill="both" ,expand=True, padx=5)
frame_pc.config(bd=0, bg="white")

# style du file explorer
style = ttk.Style()

style.configure("Treeview", font=("Arial", 12), rowheight=28)

tree = ttk.Treeview(frame_tree)
tree.heading("#0")

tree.pack(fill="both", expand=True, padx=5, pady=5)
tree.bind("<<TreeviewSelect>>", display_file_info)

# frame avec contour gris pour les informations sur le fichier
content_info = tk.Frame(frame_info, bg="white")
content_info.pack(fill="both", expand=True, padx=5, pady=5)

# frame pour les informations sur le fichier
tk.Label(content_info, text="name").pack(pady=(10,0))
entry_name = tk.Entry(content_info, state="readonly")
entry_name.pack(fill="x", padx=10, pady=(0,10))

tk.Label(content_info, text="path").pack(pady=(10, 0))
entry_path = tk.Entry(content_info, state="readonly")
entry_path.pack(fill="x", padx=10, pady=(0,10))

tk.Label(content_info, text="type").pack(pady=(10, 0))
entry_type = tk.Entry(content_info, state="readonly")
entry_type.pack(fill="x", padx=10, pady=(0,10))

tk.Label(content_info, text="size").pack(pady=(10, 0))
entry_size = tk.Entry(content_info, state="readonly")
entry_size.pack(fill="x", padx=10, pady=(0,10))

tk.Label(content_info, text="modified").pack(pady=(10, 0))
entry_date = tk.Entry(content_info, state="readonly")
entry_date.pack(fill="x", padx=10, pady=(0,10))

tk.Label(content_info, text="permissions").pack(pady=(10, 0))
entry_permissions = tk.Entry(content_info, state="readonly")
entry_permissions.pack(fill="x", padx=10, pady=(0,10))

# frame pour les informations sur le pc
content_pc = tk.Frame(frame_pc, bg="white")
content_pc.pack(fill="both", expand=True, padx=5, pady=5)

# frame pour les informations sur le processeur
frame_processors = tk.LabelFrame(content_pc, text="processors", bg="white")
frame_processors.pack(fill="x", padx=10, pady=(10, 20))
frame_processors.config(height=120)
frame_processors.pack_propagate(False)

# récupération des informations CPU
cpu_speed, cpu_uptime, cpu_usage = get_cpu_info()

# speed
row_speed = tk.Frame(frame_processors, bg="white")
row_speed.pack(fill="x", padx=10, pady=8)

tk.Label(row_speed,text="speed", bg="white").pack(side="left")

lbl_speed = tk.Label(row_speed, text=cpu_speed, bg="white")
lbl_speed.pack(side="right")

# operating time
row_uptime = tk.Frame(frame_processors, bg="white")
row_uptime.pack(fill="x", padx=10, pady=8)

tk.Label(row_uptime, text="operating time", bg="white").pack(side="left")

lbl_uptime = tk.Label(row_uptime, text=cpu_uptime, bg="white")
lbl_uptime.pack(side="right")

# use
row_usage = tk.Frame(frame_processors, bg="white")
row_usage.pack(fill="x", padx=10, pady=8)

tk.Label(row_usage, text="use", bg="white").pack(side="left")

lbl_usage = tk.Label(row_usage, text=cpu_usage, bg="white")
lbl_usage.pack(side="right")

# frame pour les informations sur le système d'exploitation
frame_os = tk.LabelFrame(content_pc, text="os", bg="white")
frame_os.pack(fill="both", expand=True, padx=10, pady=(0, 10))
frame_os.config(height=220)
frame_os.pack_propagate(False)

os_content = tk.Frame(frame_os, bg="white")
os_content.pack(fill="both", expand=True, padx=10, pady=10)

# récupération des informations sur le système d'exploitation
os_edition, os_version, os_install_date = get_os_info()

# edition
tk.Label(os_content, text="edition", bg="white").pack(pady=(10, 0))
tk.Label(os_content, text=os_edition, bg="white").pack(pady=(0, 15))

# version
tk.Label(os_content, text="version", bg="white").pack()
tk.Label(os_content, text=os_version, bg="white").pack(pady=(0, 15))

# installed
tk.Label(os_content, text="installed", bg="white").pack()
tk.Label(os_content, text=os_install_date, bg="white").pack(pady=(0, 10))

# labels pour les informations sur le processeur
refresh_cpu_info()

# la boucle principale
window.mainloop()