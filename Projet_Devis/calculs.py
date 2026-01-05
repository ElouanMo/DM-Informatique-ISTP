"""
MODULE CALCULS - LOGIQUE MÉTIER
Ce fichier contient les algorithmes de calcul de prix.
"""

# Base de données technique (Vitesse en m/min, Prix en €/kg, Densité g/cm3)
DB_MATIERES = {
    "Acier": {"vitesse": 40, "prix_kg": 3.50, "densite": 7.85},
    "Alu":   {"vitesse": 120, "prix_kg": 4.50, "densite": 2.70},
    "Inox":  {"vitesse": 25, "prix_kg": 7.00, "densite": 7.90},
    "Fonte": {"vitesse": 30, "prix_kg": 2.80, "densite": 7.20}
}

TAUX_HORAIRE_MACHINE = 75.00

def calculer_prix_devis(matiere, forme, dimension_mm, quantite):
    """
    Calcule le prix total du devis.
    """
    # 1. Récupération des infos matière
    infos = DB_MATIERES.get(matiere)
    if not infos:
        return 0.0

    vitesse_coupe = infos["vitesse"]
    prix_kg = infos["prix_kg"]
    densite = infos["densite"]

    # 2. Calcul du Coût Matière
    # On estime une section moyenne de 10 cm² pour l'exercice
    longueur_cm = dimension_mm / 10
    volume_cm3 = 10 * longueur_cm 
    poids_kg = (volume_cm3 * densite) / 1000
    cout_matiere = poids_kg * prix_kg

    # 3. Calcul du Coût Usinage
    facteur_forme = 1.2 if forme in ["Carré", "Rectangle"] else 1.0
    temps_min = (dimension_mm / vitesse_coupe) * facteur_forme
    cout_usinage = (temps_min / 60) * TAUX_HORAIRE_MACHINE

    # 4. Total avec Marge (x1.3)
    prix_unitaire = (cout_matiere + cout_usinage) * 1.3
    
    return round(prix_unitaire * quantite, 2)