from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from app.app import app, db  # Import direct après son initialisation dans app/__init__.py

from app.models.forms import LoginForm, RegisterForm  # Vérifie le bon chemin d'importation


# Création du Blueprint pour éviter d'utiliser directement `app`
# geen = Blueprint("generales", __name__)

# -------------------- ROUTES PRINCIPALES --------------------

@app.route("/")
def home():
    return render_template("partials/index.html")

@app.route("/about")
def about():
    return render_template("partials/about.html", title="À propos")

# -------------------- AUTHENTIFICATION --------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        from app.models.users import User  # Vérifie bien que ce modèle est défini
        user = User.query.filter_by(name=form.name.data).first()
        if user and check_password_hash(user.password, form.password.data):  # Sécurisé avec hashing
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for("generales.monprofil"))  # Utilisation du Blueprint
        else:
            flash("Prenom ou mot de passe incorrect.", "danger")

    return render_template("partials/login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("generales.login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        from app.models.users import User  # Vérifie bien que ce modèle est défini
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(name=form.name.data).first()
        if existing_user:
            flash("Ce name est déjà utilisé.", "danger")
            return redirect(url_for("generales.register"))

        # Création du nouvel utilisateur
        new_user = User(
            name=form.name.data,
            password=form.password.data  # ⚠️ Remplacer par un hash sécurisé avant insertion !
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Inscription réussie ! Vous pouvez vous connecter.", "success")
        return redirect(url_for("generales.login"))

    return render_template("partials/register.html", form=form)

@app.route("/monprofil")
@login_required
def monprofil():
    return render_template("partials/monprofil.html", user=current_user)

# -------------------- AUTRES PAGES --------------------

@app.route("/adaptation")
def adaptation():
    return render_template("partials/adaptation.html", title="Qu'est ce qu'une adaptation")

@app.route("/top")
def top():
    return render_template("partials/top.html", title="Top")

# -------------------- COLLECTIONS --------------------

@app.route("/collections")
def collections():
    collections = db.session.execute("SELECT id, title, user_id FROM collection").fetchall()
    return render_template("pages/collections.html", collections=collections, sous_titre="Toutes les collections")

@app.route("/collection/<int:id>")
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

@app.route("/livres")
def livres():
    livres = db.session.execute("SELECT id, title, author FROM book").fetchall()
    return render_template("pages/livres.html", livres=livres, sous_titre="Tous les livres")

@app.route("/livre/<string:id>")
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

@app.route("/films")
def films():
    films = db.session.execute("SELECT id, title, director FROM film").fetchall()
    return render_template("pages/films.html", films=films, sous_titre="Tous les films")

@app.route("/film/<string:id>")
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
