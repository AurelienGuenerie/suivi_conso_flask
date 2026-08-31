import json
import os
from flask import Flask, render_template, current_app


def create_app():
  app = Flask(__name__)

  # Route principale
  @app.route("/")
  def index():
    # Chemin vers le fichier JSON dans le dossier data externe
    # current_app.root_path pointe vers le dossier 'app/', on remonte d'un niveau pour 'data/'
    json_path = os.path.join(
        os.path.dirname(current_app.root_path), "data", "database.json"
    )

    data = {"message": "Hello World par défaut !"}
    if os.path.exists(json_path):
      with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return render_template("index.html", message=data.get("message"))

  return app