from flask_sqlalchemy import SQLAlchemy
# Importation du modèle `User` depuis `users.py`
from app.models.users import User

# Assurez-vous que `db` est également importé et initialisé ici
from app import db

# Initialize the db instance
db = SQLAlchemy()
