# from ..app import app, db, login
from app.models import db #on importe db depuis __init_.py
# from app.models import db  # Import the db instance
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin
from flask_login import UserMixin


from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Compte créé avec succès !", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title="Inscription", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("home"))
        else:
            flash("Email ou mot de passe incorrect", "danger")

    return render_template("login.html", title="Connexion", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("login"))


# class Users(UserMixin, db.Model):

class Users(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    prenom = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)  # Stocke le hash

    def check_password(self, password):
        return check_password_hash(self.password, password)  # Vérifie le hash

    @staticmethod
    def identification(prenom, password):
        utilisateur = Users.query.filter(Users.prenom == prenom).first()
        if utilisateur and check_password_hash(utilisateur.password, password):
            return utilisateur
        return None

    @staticmethod
    def ajout(prenom, password):
        erreurs = []
        if not prenom:
            erreurs.append("Le prénom est vide")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe est vide ou trop court")

        unique = Users.query.filter(
            db.or_(Users.prenom == prenom)
        ).count()
        if unique > 0:
            erreurs.append("Le prénom existe déjà")

        if len(erreurs) > 0:
            return False, erreurs
        
        utilisateur = Users(
            prenom=prenom,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        return self.id

    @login.user_loader
    def get_user_by_id(id):
        return Users.query.get(int(id))