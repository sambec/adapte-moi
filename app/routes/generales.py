from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from app import db  # Import direct après son initialisation dans app/__init__.py
from app.models.users import User  # Vérifie bien que ce modèle est défini
from app.models.forms import LoginForm, RegisterForm  # Vérifie le bon chemin d'importation
from app.routes.generales import generales_bp


# Création du Blueprint pour éviter d'utiliser directement `app`
generales_bp = Blueprint("generales", __name__)

# -------------------- ROUTES PRINCIPALES --------------------

@generales_bp.route("/")
def home():
    return render_template("partials/index.html")

@generales_bp.route("/about")
def about():
    return render_template("partials/about.html", title="À propos")

# -------------------- AUTHENTIFICATION --------------------

@generales_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(prenom=form.prenom.data).first()
        if user and check_password_hash(user.password, form.password.data):  # Sécurisé avec hashing
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("generales.monprofil"))  # Utilisation du Blueprint
        else:
            flash("Email ou mot de passe incorrect.", "danger")

    return render_template("pages/login.html", form=form)

@generales_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("generales.login"))

@generales_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for("generales.register"))

        # Création du nouvel utilisateur
        new_user = User(
            prenom=form.prenom.data,
            email=form.email.data,
            password=form.password.data  # ⚠️ Remplacer par un hash sécurisé avant insertion !
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Inscription réussie ! Vous pouvez vous connecter.", "success")
        return redirect(url_for("generales.login"))

    return render_template("pages/register.html", form=form)

@generales_bp.route("/monprofil")
@login_required
def monprofil():
    return render_template("pages/monprofil.html", user=current_user)

# -------------------- AUTRES PAGES --------------------

@generales_bp.route("/adaptation")
def adaptation():
    return render_template("partials/adaptation.html", title="Qu'est ce qu'une adaptation")

@generales_bp.route("/top")
def top():
    return render_template("partials/top.html", title="Top")

# -------------------- COLLECTIONS --------------------

@generales_bp.route("/collections")
def collections():
    collections = db.session.execute("SELECT id, title, user_id FROM collection").fetchall()
    return render_template("pages/collections.html", collections=collections, sous_titre="Toutes les collections")

@generales_bp.route("/collection/<int:id>")
def collection_specifique(id):
    collection = db.session.execute(
        "SELECT id, title, user_id, description FROM collection WHERE id = :id", {"id": id}
    ).fetchone()
    
    if not collection:
        return render_template("pages/404.html"), 404

    films = db.session.execute(
        "SELECT film.id, film.title FROM film "
        "JOIN collection_film ON film.id = collection_film.id_film "
        "WHERE collection_film.id_collection = :id", {"id": id}
    ).fetchall()

    return render_template("pages/collection.html", collection=collection, films=films, sous_titre=collection.title)

# -------------------- LIVRES --------------------

@generales_bp.route("/livres")
def livres():
    livres = db.session.execute("SELECT id, title, author FROM book").fetchall()
    return render_template("pages/livres.html", livres=livres, sous_titre="Tous les livres")

@generales_bp.route("/livre/<string:id>")
def livre_specifique(id):
    livre = db.session.execute(
        "SELECT id, title, author FROM book WHERE id = :id", {"id": id}
    ).fetchone()
    
    if not livre:
        return render_template("pages/404.html"), 404

    films = db.session.execute(
        "SELECT film.id, film.title FROM film "
        "JOIN book_film ON film.id = book_film.id_film "
        "WHERE book_film.id_livre = :id", {"id": id}
    ).fetchall()

    return render_template("pages/livre.html", livre=livre, films=films, sous_titre=livre.title)

# -------------------- FILMS --------------------

@generales_bp.route("/films")
def films():
    films = db.session.execute("SELECT id, title, director FROM film").fetchall()
    return render_template("pages/films.html", films=films, sous_titre="Tous les films")

@generales_bp.route("/film/<string:id>")
def film_specifique(id):
    film = db.session.execute(
        "SELECT id, title, director FROM film WHERE id = :id", {"id": id}
    ).fetchone()
    
    if not film:
        return render_template("pages/404.html"), 404

    livres = db.session.execute(
        "SELECT book.id, book.title FROM book "
        "JOIN book_film ON book.id = book_film.id_livre "
        "WHERE book_film.id_film = :id", {"id": id}
    ).fetchall()

    return render_template("pages/film.html", film=film, livres=livres, sous_titre=film.title)
