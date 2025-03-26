from ..app import app, db
from flask import render_template, request
from sqlalchemy import or_, select
from ..models.adapte_moi import Film, Book, film_book
# from ..models.formulaires import Recherche

# GESTION ERREURS
@app.errorhandler(404)
def page_not_found(error):
    return render_template('partials/404.html'), 404

# REDIRECTION ACCUEIL
@app.route("/")
@app.route("/index")
@app.route("/index.html")
@app.route("/accueil")
def home():
    # return app/statics/test.pyredirect(url_for("index"))
    return render_template("partials/index.html")

@app.route("/about")
def about():
    # return app/statics/test.pyredirect(url_for("index"))
    return render_template("partials/about.html")

@app.route("/adaptation")
@app.route("/adaptation.html")
def adaptation():
    # return app/statics/test.pyredirect(url_for("index"))
    return render_template("partials/adaptation.html")

@app.route("/top")
@app.route("/top.html")
def top():
    return render_template("partials/top.html")

# Afficher la liste des livres présents dans la base de données
@app.route('/books')
def list_books():
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Nombre de livres par page
    books_paginated = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('pages/books.html', books=books_paginated)