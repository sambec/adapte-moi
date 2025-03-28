from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# On va plutôt mettre les utilisateurs dans un fichier à part
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)

# mais je pense qu'on peut mettre les livres et les films dans le même fichier ? à voir selon le modèle UML
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    wikipedia_link = db.Column(db.String(500))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    recommendation_index = db.Column(db.Float)
