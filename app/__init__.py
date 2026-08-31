from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import et enregistrement des routes directement depuis le fichier routes.py
    from app.routes import main_bp
    app.register_blueprint(main_bp)
        
    return app