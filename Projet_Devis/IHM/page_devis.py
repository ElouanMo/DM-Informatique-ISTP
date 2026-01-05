import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import data_manager
import calculs

def afficher(parent):
    # Fenêtre
    fenetre = tb.Toplevel(parent)
    fenetre.title("Nouveau Devis")
    fenetre.geometry("900x650")
    
    fenetre.columnconfigure(0, weight=2)
    fenetre.columnconfigure(1, weight=1)
    fenetre.rowconfigure(0, weight=1)

    # --- COLONNE GAUCHE ---
    left_panel = tb.Frame(fenetre, padding=20)
    left_panel.grid(row=0, column=0, sticky="nsew")

    tb.Label(left_panel, text="CONFIGURATION TECHNIQUE", font=("Helvetica", 16, "bold"), bootstyle="info").pack(anchor="w", pady=(0, 20))

    # Bloc Client (Correction Labelframe)
    frame_cli = tb.Labelframe(left_panel, text="  Projet & Client  ", padding=15, bootstyle="info")
    frame_cli.pack(fill=X, pady=10)
    
    tb.Label(frame_cli, text="Client :").pack(anchor="w")
    
    # Sécurité pour charger les clients
    try:
        liste_clients = data_manager.get_all_clients_str()
    except AttributeError:
        liste_clients = ["Erreur: data_manager non mis à jour"]

    combo_client = tb.Combobox(frame_cli, values=liste_clients, state="readonly", bootstyle="info")
    combo_client.pack(fill=X, pady=(5, 15))

    tb.Label(frame_cli, text="Description :").pack(anchor="w")
    entry_desc = tb.Entry(frame_cli)
    entry_desc.pack(fill=X, pady=5)

    # Bloc Technique (Correction Labelframe)
    frame_tech = tb.Labelframe(left_panel, text="  Usinage  ", padding=15, bootstyle="warning")
    frame_tech.pack(fill=X, pady=10)

    tb.Label(frame_tech, text="Matière").grid(row=0, column=0, sticky="w", padx=5)
    tb.Label(frame_tech, text="Forme").grid(row=0, column=1, sticky="w", padx=5)
    
    combo_matiere = tb.Combobox(frame_tech, values=["Acier", "Alu", "Inox", "Fonte"], state="readonly", bootstyle="warning")
    combo_matiere.current(0)
    combo_matiere.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
    
    combo_forme = tb.Combobox(frame_tech, values=["Rond", "Carré", "Rectangle"], state="readonly", bootstyle="warning")
    combo_forme.current(0)
    combo_forme.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

    tb.Label(frame_tech, text="Dimension (mm)").grid(row=2, column=0, sticky="w", padx=5)
    tb.Label(frame_tech, text="Quantité").grid(row=2, column=1, sticky="w", padx=5)

    entry_dim = tb.Entry(frame_tech)
    entry_dim.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")

    entry_qte = tb.Entry(frame_tech)
    entry_qte.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")
    
    frame_tech.columnconfigure(0, weight=1)
    frame_tech.columnconfigure(1, weight=1)

    # --- COLONNE DROITE ---
    right_panel = tb.Frame(fenetre, bootstyle="secondary", padding=20)
    right_panel.grid(row=0, column=1, sticky="nsew")

    tb.Label(right_panel, text="TOTAL ESTIMÉ", font=("Helvetica", 14), bootstyle="inverse-secondary").pack(pady=20)
    
    var_total = tb.StringVar(value="0.00 €")
    lbl_prix = tb.Label(right_panel, textvariable=var_total, font=("Helvetica", 32, "bold"), bootstyle="success-inverse")
    lbl_prix.pack(pady=10)

    tb.Separator(right_panel, bootstyle="light").pack(fill=X, pady=20)

    def action_calculer():
        try:
            mat = combo_matiere.get()
            forme = combo_forme.get()
            dim = float(entry_dim.get())
            qte = int(entry_qte.get())
            prix = calculs.calculer_prix_devis(mat, forme, dim, qte)
            var_total.set(f"{prix:.2f} €")
        except ValueError:
            messagebox.showerror("Erreur", "Vérifiez les valeurs numériques.")

    btn_calcul = tb.Button(right_panel, text="⚡ CALCULER", bootstyle="light-outline", width=20, command=action_calculer)
    btn_calcul.pack(pady=10)

    tb.Label(right_panel, text="", bootstyle="inverse-secondary").pack(expand=True)

    def action_sauvegarder():
        client = combo_client.get()
        prix_str = var_total.get().replace(" €", "")
        if not client or "Erreur" in client:
            messagebox.showwarning("Erreur", "Client invalide")
            return
        if float(prix_str) == 0:
            messagebox.showwarning("Erreur", "Montant nul")
            return
            
        data = {
            "client": client, "description": entry_desc.get(),
            "matiere": combo_matiere.get(), "forme": combo_forme.get(),
            "dimension": entry_dim.get(), "quantite": entry_qte.get(),
            "prix_total": prix_str
        }
        data_manager.save_devis(data)
        messagebox.showinfo("Succès", "Devis validé !")
        fenetre.destroy()

    btn_save = tb.Button(right_panel, text="💾  VALIDER", bootstyle="success", width=20, command=action_sauvegarder)
    btn_save.pack(pady=20, ipady=10)

    btn_close = tb.Button(right_panel, text="Fermer", bootstyle="secondary", command=fenetre.destroy)
    btn_close.pack()