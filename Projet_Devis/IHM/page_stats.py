import ttkbootstrap as tb
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import reporting

def afficher(parent):
    # Fenêtre Toplevel
    fenetre = tb.Toplevel(parent)
    fenetre.title("Analyse & Reporting")
    fenetre.geometry("1100x700")
    
    # Entête
    header = tb.Frame(fenetre, padding=20)
    header.pack(fill=X)
    tb.Label(header, text="TABLEAU DE BORD", font=("Impact", 24), bootstyle="info").pack(side=LEFT)
    tb.Button(header, text="Fermer", bootstyle="secondary-outline", command=fenetre.destroy).pack(side=RIGHT)

    # Zone de contenu
    content = tb.Frame(fenetre, padding=20)
    content.pack(fill=BOTH, expand=True)

    try:
        # On récupère les 2 figures créées dans reporting.py
        fig_devis, fig_dept = reporting.create_figures()

        # --- GRAPHIQUE 1 (GAUCHE) ---
        frame_g = tb.Labelframe(content, text="  Analyse Financière  ", bootstyle="warning", padding=10)
        frame_g.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # Le composant magique qui transforme un graphique Matplotlib en Widget Tkinter
        canvas1 = FigureCanvasTkAgg(fig_devis, master=frame_g)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True)

        # --- GRAPHIQUE 2 (DROITE) ---
        frame_d = tb.Labelframe(content, text="  Analyse Géographique  ", bootstyle="info", padding=10)
        frame_d.pack(side=LEFT, fill=BOTH, expand=True, padx=(10, 0))
        
        canvas2 = FigureCanvasTkAgg(fig_dept, master=frame_d)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=BOTH, expand=True)

    except Exception as e:
        tb.Label(content, text=f"Erreur d'affichage des graphiques :\n{e}", bootstyle="danger").pack()