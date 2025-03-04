from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from .config import Config
from app.models import db  # Assuming you have db setup in a models file
from app.routes.generales import generales_bp  # Import your Blueprint


# Initialisation des extensions (sans les lier encore à app)
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Configure your app (e.g., secret key, database URI)
    app.config['SECRET_KEY'] = 'blop'
    app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////adapte_moi.sqlite'

    # Initialize extensions like the db and login_manager
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(generales_bp)

    # Return the app instance
    return app
