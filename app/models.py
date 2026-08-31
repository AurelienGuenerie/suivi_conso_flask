import json
import os
from flask import current_app

# __file__ est ce fichier (models.py)
# os.path.dirname(...) -> dossier 'app/'
# on remonte encore avec un autre os.path.dirname(...) -> dossier racine 'conso/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'database.json')


def calculer_conso(plein: float, compteur: float):
    """ Calcul la consommation
    
    Returns:
        float: la consommation arrondi à 2 décimales
    """
    if compteur == 0: return 0
    
    conso = round(plein/compteur*100,2)
    return conso


def ajouter_ligne_dico(date, plein, compteur, conso):
    # S'assurer que le dossier data existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Charger les données existantes si le fichier existe
    suivi = {}
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as file:
                suivi = json.load(file)
        except json.JSONDecodeError:
            suivi = {}

    # Ajouter ou mettre à jour l'entrée
    suivi[date] = {
        'plein': plein,
        'compteur': compteur,
        'consommation': conso
    }

    # Sauvegarder dans le fichier
    with open(DB_PATH, 'w', encoding='utf-8') as file:
        json.dump(suivi, file, indent=4, ensure_ascii=False)
    
    print(f"Nouvelle date créée : {date}")
    
def recuperer_donnees():
    if not os.path.exists(DB_PATH):
        return {}
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as file:
            suivi = json.load(file)
            # Tri par date (les clés du dictionnaire)
            return dict(sorted(suivi.items()))
    except json.JSONDecodeError:
        return {}
    
def supprimer_ligne_dico(date):
    if not os.path.exists(DB_PATH):
        return
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as file:
            suivi = json.load(file)
    except json.JSONDecodeError:
        suivi = {}

    if date in suivi:
        del suivi[date]
        with open(DB_PATH, 'w', encoding='utf-8') as file:
            json.dump(suivi, file, indent=4, ensure_ascii=False)
        print(f"Entrée supprimée : {date}")