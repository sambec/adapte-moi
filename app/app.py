from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from .config import Config #normalement pas de boucles infinies avec config donc tout va bien


# Initialisation de Flask
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='statics'
)
app.config.from_object(Config)

# Initialisation des extensions
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
# login_manager.login_view = "login"

# # ⚠️ Importation des modèles et routes APRES l'initialisation de db
# from app.routes.generales import generales_bp  
# app.register_blueprint(generales_bp)

# Définition du user_loader après l'initialisation de login_manager
@login_manager.user_loader
def load_user(user_id):
    from app.models.users import Users  # Import local pour éviter l'import circulaire
    return Users.get(user_id)
# @login_manager.user_loader
# def load_user(user_id):
#     from app.models.users import User  # Import local pour éviter l'import circulaire
#     return User.query.get(int(user_id))

# 🚨 **IMPORTANT** : Importer les routes *SEULEMENT APRÈS* l'initialisation complète
from app.routes.generales import *


