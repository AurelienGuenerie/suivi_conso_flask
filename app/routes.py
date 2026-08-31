from flask import Blueprint, render_template, request, redirect, url_for
from app.models import *

main_bp = Blueprint('main', __name__)

@main_bp.route('/', defaults={'vehicle': None}, methods=['GET', 'POST'])
@main_bp.route('/<vehicle>', methods=['GET', 'POST'])
def index(vehicle):
    # 1. Charger l'ensemble des données (qui contient tous les véhicules)
    toutes_les_donnees = recuperer_donnees() # Renvoie ex: {"Clio": {...}, "Partner": {...}}
    list_vehicles = list(toutes_les_donnees.keys())

    # Sécurité si aucun véhicule n'existe encore
    if not list_vehicles:
        list_vehicles = ['Clio'] # Véhicule par défaut initial

    # Déterminer le véhicule actif
    if not vehicle or vehicle not in list_vehicles:
        current_vehicle = list_vehicles[0]
        if not request.args.get('vehicle') and not vehicle:
            return redirect(url_for('main.index', vehicle=current_vehicle))
    else:
        current_vehicle = vehicle

    # 2. Traitement du formulaire (POST)
    if request.method == 'POST':
        # On récupère le véhicule actif depuis le champ caché du formulaire
        active_vehicle = request.form.get('vehicle', current_vehicle)
        date = request.form.get('date')
        plein = float(request.form.get('plein', 0))
        compteur = float(request.form.get('compteur', 0))
        
        conso = calculer_conso(plein, compteur)

        # Enregistrement en précisant le véhicule dans vos models
        ajouter_ligne_dico(active_vehicle, date, plein, compteur, conso)
        
        return redirect(url_for('main.index', vehicle=active_vehicle))

    # 3. Récupération de l'historique propre au véhicule actif (GET)
    historique = toutes_les_donnees.get(current_vehicle, {})
    
    return render_template(
        'index.html', 
        title="Suivi Consommation", 
        historique=historique,
        list_vehicles=list_vehicles,
        current_vehicle=current_vehicle
    )

@main_bp.route('/delete/<vehicle>/<date>', methods=['POST'])
def delete(vehicle, date):
    supprimer_ligne_dico(vehicle, date)
    return redirect(url_for('main.index', vehicle=vehicle))

@main_bp.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    new_vehicle = request.form.get('new_vehicle_name', '').strip()
    if new_vehicle:
        # Charger les données existantes
        donnees_globales = recuperer_donnees()
        
        # Si le véhicule n'existe pas encore, on l'initialise avec un dictionnaire vide
        if new_vehicle not in donnees_globales:
            donnees_globales[new_vehicle] = {}
            
            # Sauvegarder dans le fichier JSON
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            with open(DB_PATH, 'w', encoding='utf-8') as file:
                json.dump(donnees_globales, file, indent=4, ensure_ascii=False)
                
        # Rediriger directement sur la page de ce nouveau véhicule
        return redirect(url_for('main.index', vehicle=new_vehicle))
        
    return redirect(url_for('main.index'))

@main_bp.route('/delete_vehicle/<vehicle>', methods=['POST'])
def delete_vehicle(vehicle):
    donnees_globales = recuperer_donnees()
    
    if vehicle in donnees_globales:
        del donnees_globales[vehicle]
        
        # Sauvegarder la mise à jour
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, 'w', encoding='utf-8') as file:
            json.dump(donnees_globales, file, indent=4, ensure_ascii=False)
            
    # Rediriger vers un autre véhicule s'il en reste, sinon retour à la racine
    restants = list(donnees_globales.keys())
    if restants:
        return redirect(url_for('main.index', vehicle=restants[0]))
    return redirect(url_for('main.index'))