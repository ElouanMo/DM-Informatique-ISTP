import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import data_manager

def afficher(parent):
    fenetre = tb.Toplevel(parent)
    fenetre.title("Gestion Base Clients")
    fenetre.geometry("600x650")

    # Conteneur principal
    main_frame = tb.Frame(fenetre, padding=20)
    main_frame.pack(fill=BOTH, expand=True)

    # Titre
    tb.Label(main_frame, text="NOUVEAU PARTENAIRE", font=("Helvetica", 18, "bold"), bootstyle="warning").pack(pady=(0,20))

    # --- CORRECTION ICI : "Labelframe" avec un 'f' minuscule ---
    form_box = tb.Labelframe(main_frame, text="  Coordonnées  ", padding=20, bootstyle="secondary")
    form_box.pack(fill=BOTH, expand=True)

    entries = {}
    champs = [
        ("Société", "raison_sociale"), ("Nom Contact", "nom"), 
        ("Prénom", "prenom"), ("E-mail", "email"), 
        ("Téléphone", "tel"), ("Ville", "ville")
    ]

    for lbl_txt, key in champs:
        row = tb.Frame(form_box)
        row.pack(fill=X, pady=5)
        # Label à gauche
        tb.Label(row, text=lbl_txt, width=15).pack(side=LEFT)
        # Champ de saisie à droite
        entry = tb.Entry(row, bootstyle="dark")
        entry.pack(side=RIGHT, expand=True, fill=X)
        entries[key] = entry

    # Boutons
    btn_box = tb.Frame(main_frame, padding=20)
    btn_box.pack(fill=X)

    def save():
        data = {
            "raison_sociale": entries["raison_sociale"].get(), "nom": entries["nom"].get(),
            "prenom": entries["prenom"].get(), "email": entries["email"].get(),
            "tel": entries["tel"].get(), "adresse": "", "cp": "", "ville": entries["ville"].get()
        }
        
        # Validation simple
        if not data["raison_sociale"]:
            messagebox.showwarning("Attention", "Le nom de la Société est obligatoire")
            return
            
        data_manager.save_client(data)
        messagebox.showinfo("Succès", "Client ajouté à la base !")
        fenetre.destroy()

    btn_save = tb.Button(btn_box, text="AJOUTER BASE", bootstyle="warning", width=20, command=save) 
    btn_save.pack(side=RIGHT)
    
    btn_close = tb.Button(btn_box, text="Annuler", bootstyle="secondary", command=fenetre.destroy)
    btn_close.pack(side=RIGHT, padx=10)