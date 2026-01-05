import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os

# Chemins des fichiers
DATA_DIR = "DATA"
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.csv")
DEVIS_FILE = os.path.join(DATA_DIR, "devis.csv")

# Couleurs du thème (pour aller avec le style PERL)
COLOR_TEXT = "#ffffff"       # Texte blanc
COLOR_BG = "#2b3e50"         # Gris bleu foncé (fond de la fenêtre)
COLOR_BAR = "#df691a"        # Orange (couleur 'warning' du thème)
COLOR_PIE = ["#df691a", "#5bc0de", "#f0ad4e", "#d9534f", "#5cb85c"] # Palette

def get_stats_data():
    """ Lit les CSV et prépare les données mathématiques """
    
    # --- 1. DONNÉES DEVIS ---
    stats_devis = {"0-1k €": 0, "1k-5k €": 0, "5k-10k €": 0, "> 10k €": 0}
    
    if os.path.exists(DEVIS_FILE):
        try:
            # On lit le CSV avec Pandas
            df = pd.read_csv(DEVIS_FILE)
            # On nettoie la colonne prix (enlève le '€' si présent et convertit en nombre)
            if not df.empty and "Prix_Total" in df.columns:
                # Convertir en string, nettoyer, puis convertir en float
                prix_clean = df["Prix_Total"].astype(str).str.replace(' €', '').str.replace(',', '.')
                prix_col = pd.to_numeric(prix_clean, errors='coerce')
                
                for prix in prix_col:
                    if pd.isna(prix): continue
                    if prix <= 1000: stats_devis["0-1k €"] += 1
                    elif prix <= 5000: stats_devis["1k-5k €"] += 1
                    elif prix <= 10000: stats_devis["5k-10k €"] += 1
                    else: stats_devis["> 10k €"] += 1
        except Exception as e:
            print(f"Erreur Devis: {e}")

    # --- 2. DONNÉES CLIENTS (DÉPARTEMENTS) ---
    stats_dept = {}
    if os.path.exists(CLIENTS_FILE):
        try:
            df = pd.read_csv(CLIENTS_FILE)
            # On vérifie que la colonne CP existe (selon votre code précédent c'est 'Code_Postal' ou 'cp')
            # Pandas est sensible à la casse, on essaie de trouver la bonne colonne
            col_cp = None
            for c in df.columns:
                if "cp" in c.lower() or "postal" in c.lower():
                    col_cp = c
                    break
            
            if col_cp:
                # On prend les 2 premiers chiffres (ex: 42000 -> 42)
                deps = df[col_cp].astype(str).str[:2]
                stats_dept = deps.value_counts().head(5).to_dict() # Top 5 départements
        except Exception as e:
            print(f"Erreur Clients: {e}")
            
    return stats_devis, stats_dept

def create_figures():
    """ Crée les graphiques Matplotlib """
    data_devis, data_dept = get_stats_data()
    
    # Configuration globale pour le mode sombre
    plt.rcParams.update({
        'text.color': COLOR_TEXT,
        'axes.labelcolor': COLOR_TEXT,
        'xtick.color': COLOR_TEXT,
        'ytick.color': COLOR_TEXT,
        'axes.edgecolor': COLOR_TEXT
    })

    # --- FIGURE 1 : Histogramme Devis ---
    fig1 = Figure(figsize=(5, 4), dpi=100, facecolor=COLOR_BG)
    ax1 = fig1.add_subplot(111)
    ax1.set_facecolor(COLOR_BG) # Fond du graphique
    
    categories = list(data_devis.keys())
    valeurs = list(data_devis.values())
    
    ax1.bar(categories, valeurs, color=COLOR_BAR)
    ax1.set_title("Répartition des Montants Devis", color=COLOR_TEXT, fontsize=12, pad=20)
    ax1.set_ylabel("Nombre de dossiers")
    ax1.tick_params(axis='x', rotation=15)

    # --- FIGURE 2 : Camembert Départements ---
    fig2 = Figure(figsize=(5, 4), dpi=100, facecolor=COLOR_BG)
    ax2 = fig2.add_subplot(111)
    
    if data_dept:
        labels = list(data_dept.keys())
        sizes = list(data_dept.values())
        # Camembert
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                           startangle=90, colors=COLOR_PIE)
        # Changer la couleur du texte dans le camembert
        for text in texts + autotexts:
            text.set_color(COLOR_TEXT)
    else:
        ax2.text(0.5, 0.5, "Pas assez de données clients", ha='center', va='center', color=COLOR_TEXT)

    ax2.set_title("Top Départements Clients", color=COLOR_TEXT, fontsize=12)
    
    return fig1, fig2