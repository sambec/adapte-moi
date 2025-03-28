from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

class AjoutUtilisateur(FlaskForm):
    pseudo = StringField("pseudo", validators=[])
    password = PasswordField("password", validators=[])

class Connexion(FlaskForm):
    pseudo = StringField("pseudo", validators=[])
    password = PasswordField("password", validators=[])