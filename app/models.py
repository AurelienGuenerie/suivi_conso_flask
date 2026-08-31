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


def ajouter_ligne_dico(vehicule: str, date: str | None, plein: float, compteur: float, conso: float):
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
            
     # 1. S'assurer que le dictionnaire pour ce véhicule existe
    if vehicule not in suivi:
        suivi[vehicule] = {}
            
    # 2. Ajouter ou mettre à jour l'entrée pour ce véhicule spécifique
    suivi[vehicule][date] = {
        'plein': plein,
        'compteur': compteur,
        'consommation': conso
    }

    # Sauvegarder dans le fichier
    with open(DB_PATH, 'w', encoding='utf-8') as file:
        json.dump(suivi, file, indent=4, ensure_ascii=False)
    
    print(f"Nouvelle date créée pour {vehicule} : {date}")  
      
def recuperer_donnees():
    if not os.path.exists(DB_PATH):
            return {}
            
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not data:
                return {}
            
            # Vérifier si c'est l'ancienne structure (les valeurs contiennent directement 'plein')
            premiere_cle = next(iter(data))
            if isinstance(data[premiere_cle], dict) and "plein" in data[premiere_cle]:
                # Migration automatique vers la nouvelle structure multi-véhicules
                data = {"Restauration": data}
                
                # Sauvegarder tout de suite la structure mise à jour dans le fichier
                with open(DB_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    
            return data
    except json.JSONDecodeError:
        return {}
    
def supprimer_ligne_dico(vehicule: str, date: str):
    if not os.path.exists(DB_PATH):
        return
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as file:
            suivi = json.load(file)
    except json.JSONDecodeError:
        suivi = {}

    if vehicule in suivi:
        if date in suivi[vehicule]:
            del suivi[vehicule][date]
            
            # Optionnel : supprimer la clé du véhicule si elle est vide
            if not suivi[vehicule]:
                del suivi[vehicule]
            
            with open(DB_PATH, 'w', encoding='utf-8') as file:
                json.dump(suivi, file, indent=4, ensure_ascii=False)
            print(f"Entrée supprimée : {date}")