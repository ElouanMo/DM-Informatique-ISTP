import csv
import os

DATA_DIR = "DATA"
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.csv")
DEVIS_FILE = os.path.join(DATA_DIR, "devis.csv")

# En-têtes
ENTETES_CLIENTS = ["ID_Client", "Raison_Sociale", "Nom_Contact", "Prenom_Contact", "Email", "Telephone", "Adresse", "Code_Postal", "Ville"]
ENTETES_DEVIS = ["ID_Devis", "Client_Str", "Description", "Matiere", "Forme", "Dimension", "Quantite", "Prix_Total"]

def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(ENTETES_CLIENTS)
    if not os.path.exists(DEVIS_FILE):
        with open(DEVIS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(ENTETES_DEVIS)

def get_next_id(filename):
    if not os.path.exists(filename): return 1
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        if len(data) <= 1: return 1
        try: return int(data[-1][0]) + 1
        except: return 1

def save_client(client_data):
    new_id = get_next_id(CLIENTS_FILE)
    row = [
        new_id, client_data.get("raison_sociale", "").upper(), client_data.get("nom", "").upper(),
        client_data.get("prenom", "").capitalize(), client_data.get("email", ""), client_data.get("tel", ""),
        client_data.get("adresse", ""), client_data.get("cp", ""), client_data.get("ville", "").upper()
    ]
    with open(CLIENTS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    return new_id

# --- C'EST CETTE FONCTION QUI MANQUAIT PEUT-ÊTRE ---
def get_all_clients_str():
    """Renvoie une liste 'ID - Nom' pour le menu déroulant."""
    clients_list = []
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clients_list.append(f"{row['ID_Client']} - {row['Raison_Sociale']}")
    return clients_list

def save_devis(devis_data):
    new_id = get_next_id(DEVIS_FILE)
    row = [
        new_id, devis_data.get("client", ""), devis_data.get("description", ""),
        devis_data.get("matiere", ""), devis_data.get("forme", ""),
        devis_data.get("dimension", ""), devis_data.get("quantite", ""),
        devis_data.get("prix_total", "")
    ]
    with open(DEVIS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    return new_id

if __name__ == "__main__":
    init_db()