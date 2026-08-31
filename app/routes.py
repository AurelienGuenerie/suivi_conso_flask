from flask import Blueprint, render_template, request, redirect, url_for
from app.models import *

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        plein = float(request.form.get('plein', 0))
        compteur = float(request.form.get('compteur', 0))
        
        # Logique de calcul simple ou mise à zéro en attendant
        conso = calculer_conso(plein, compteur)

        # Enregistrement via models.py
        ajouter_ligne_dico(date, plein, compteur, conso)
        
        return redirect(url_for('main.index'))

    # Récupération de l'historique pour l'affichage
    historique = recuperer_donnees()
    
    return render_template('index.html', title="Suivi Consommation", historique=historique)

@main_bp.route('/delete/<date>', methods=['POST'])
def delete(date):
    supprimer_ligne_dico(date)
    return redirect(url_for('main.index'))