from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired



class LoginForm(FlaskForm):
    prenom = StringField('Prénom', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    prenom = StringField("Nom d'utilisateur", validators=[InputRequired(), Length(min=4, max=100)])
    password = PasswordField("Mot de passe", validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmez le mot de passe", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("S'inscrire")