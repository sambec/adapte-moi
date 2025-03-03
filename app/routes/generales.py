from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user
from ..models.forms import * # Assurez-vous que le chemin d'importation est correct


# from ..models.formulaires import Recherche


@app.route("/")
def home():
    return render_template("partials/index.html")

@app.route("/about")
def about():
    return render_template("partials/about.html", title="À propos")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Ajoutez ici la logique pour vérifier les informations d'identification de l'utilisateur
        # Par exemple, vérifiez le prénom et le mot de passe dans la base de données
        # Si les informations sont correctes, connectez l'utilisateur
            flash('Connexion réussie !')
            return redirect(url_for('home'))
        # pass
    return render_template("partials/login.html", title="Se connecter", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Ajoutez ici la logique pour enregistrer le nouvel utilisateur dans la base de données
        flash('Inscription réussie !')
        return redirect(url_for('login'))
    return render_template("partials/register.html", title="S'inscrire", form=form)


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
    collection = db.session.execute("SELECT id, title, user_id, description FROM collection WHERE id = :id", {"id": id}).fetchone()
    films = db.session.execute(
        "SELECT film.id, film.title FROM film "
        "JOIN collection_film ON film.id = collection_film.id_film "
        "WHERE collection_film.id_collection = :id",
        {"id": id}
    ).fetchall()
    if not collection:
        return render_template("pages/404.html"), 404
    return render_template("pages/collection.html", collection=collection, films=films, sous_titre=collection.title)


# -------------------- LIVRES --------------------

@app.route("/livres")
def livres():
    livres = db.session.execute("SELECT id, title, author FROM book").fetchall()
    return render_template("pages/livres.html", livres=livres, sous_titre="Tous les livres")


@app.route("/livre/<string:id>")
def livre_specifique(id):
    livre = db.session.execute("SELECT id, title, author FROM book WHERE id = :id", {"id": id}).fetchone()
    films = db.session.execute(
        "SELECT film.id, film.title FROM film "
        "JOIN book_film ON film.id = book_film.id_film "
        "WHERE book_film.id_livre = :id",
        {"id": id}
    ).fetchall()
    if not livre:
        return render_template("pages/404.html"), 404
    return render_template("pages/livre.html", livre=livre, films=films, sous_titre=livre.title)


# -------------------- FILMS --------------------

@app.route("/films")
def films():
    films = db.session.execute("SELECT id, title, director FROM film").fetchall()
    return render_template("pages/films.html", films=films, sous_titre="Tous les films")


@app.route("/film/<string:id>")
def film_specifique(id):
    film = db.session.execute("SELECT id, title, director FROM film WHERE id = :id", {"id": id}).fetchone()
    livres = db.session.execute(
        "SELECT book.id, book.title FROM book "
        "JOIN book_film ON book.id = book_film.id_livre "
        "WHERE book_film.id_film = :id",
        {"id": id}
    ).fetchall()
    if not film:
        return render_template("pages/404.html"), 404
    return render_template("pages/film.html", film=film, livres=livres, sous_titre=film.title)
