from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
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

@login_manager.user_loader
def load_user(user_id):
    from app.models.users import User  # Importation locale pour éviter les importations circulaires
    return User.query.get(int(user_id))

# Importer les routes après l'init
# from app import routes  # Assurez-vous que 'routes' est le bon module à importer
from app.routes.generales import *

