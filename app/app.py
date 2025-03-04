from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from .config import Config

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
login_manager.login_view = "login"

# Définition du user_loader après l'initialisation de login_manager
@login_manager.user_loader
def load_user(user_id):
    from app.models.users import User  # Import local pour éviter l'import circulaire
    return User.query.get(int(user_id))

# 🚨 **IMPORTANT** : Importer les routes *SEULEMENT APRÈS* l'initialisation complète
from app.routes import generales  # NE PAS IMPORTER "*" -> ça cause des erreurs d'import
