from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, PasswordField

class AjoutUtilisateur(FlaskForm):
    pseudo = StringField("pseudo", validators=[])
    password = PasswordField("password", validators=[])