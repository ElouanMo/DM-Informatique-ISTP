import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

# Importation de vos pages
from IHM import page_clients, page_devis, page_stats

class Application(tb.Window):
    def __init__(self):
        # Thème sombre industriel
        super().__init__(themename="superhero")

        import data_manager
        data_manager.init_db()

        self.title("ALGORITHMIE - Gestion Devis")
        self.geometry("1000x700")
        
        # Configuration de la grille : La colonne 1 (droite) prend toute la place restante
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # --- BARRE LATERALE (GAUCHE) ---
        self.sidebar = tb.Frame(self, bootstyle="secondary", padding=20, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False) # Bloque la largeur pour qu'elle ne bouge pas

        # Titre App (Sidebar)
        lbl_app = tb.Label(self.sidebar, text="APPLICATION\nPERL", font=("Impact", 20), bootstyle="inverse-secondary", justify="center")
        lbl_app.pack(pady=(0, 40))

        # Boutons de navigation
        self.create_sidebar_button("👤  CLIENTS", "info", self.ouvrir_clients)
        self.create_sidebar_button("📝  DEVIS", "info", self.ouvrir_devis)
        self.create_sidebar_button("📊  STATS", "info", self.ouvrir_stats)
        
        # Espaceur (pousse le bouton Quitter vers le bas)
        tb.Label(self.sidebar, text="").pack(expand=True)
        
        self.create_sidebar_button("❌  QUITTER", "danger", self.quit)

        # --- ZONE PRINCIPALE (DROITE) ---
        # Cette zone est maintenant propre et vide
        self.main_area = tb.Frame(self, padding=20)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        # Juste un logo discret au centre pour l'accueil
        lbl_watermark = tb.Label(self.main_area, text="PERL", font=("Helvetica", 60, "bold"), bootstyle="secondary")
        lbl_watermark.place(relx=0.5, rely=0.45, anchor="center") # Centré
        
        lbl_sub = tb.Label(self.main_area, text="Logiciel de Gestion", font=("Helvetica", 20), bootstyle="secondary")
        lbl_sub.place(relx=0.5, rely=0.55, anchor="center")

    def create_sidebar_button(self, text, style, command):
        btn = tb.Button(
            self.sidebar, 
            text=text, 
            bootstyle=f"{style}-outline", 
            width=20, 
            command=command
        )
        btn.pack(pady=10, ipady=5)

    def ouvrir_clients(self):
        page_clients.afficher(self)

    def ouvrir_devis(self):
        page_devis.afficher(self)
        
    def ouvrir_stats(self):
        page_stats.afficher(self)

if __name__ == "__main__":
    app = Application()
    app.mainloop()