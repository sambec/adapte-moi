from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify, request
from sqlalchemy import or_, select
from ..models.adapte_moi import Film, Book, film_book
import random
# from ..models.formulaires import Recherche
# from ..utils.transformations import nettoyage_string_to_int, clean_arg

# @app.route("/test_book")
# def test_book():
#     books = []
#     for book in Book.query.all():
#         books.append(book.title)
#     return render_template("pages/test.html", livres=books)


@app.route("/livres")
def pays(page=1):
    return render_template("pages/livres.html", 
        sous_titre="Livres", 
        donnees= Book.query.order_by(Book.title).paginate(page=page, per_page=app.config["BOOK_PER_PAGE"]))


# ROUTE SIMPLE pour récupérer les informations d'un seul livre
@app.route("/book/<string:book_name>")
def get_book(book_name):
    book = Book.query.filter_by(title=book_name).first()
    if book:
        return render_template("pages/livre.html", livre=book.title, auteur=book.author)
    else:
        return "Livre non trouvé", 404


# Route simple pour récupérer les informations d'un auteur
@app.route("/author/<string:author_name>")
def get_author(author_name):
    author = Book.query.filter_by(author=author_name).first()
    if author:
        return render_template("pages/auteur.html", auteur=author.author)
    else:
        return "auteur non trouvé", 404


# Route search pour effectuer une recherche dans la BDD
@app.route("/search", methods=['GET', 'POST'])
def search():
    titles = ""
    if request.method == "POST":
        donnees = request.form
        # print(donnees)
        my_title = donnees.get("title")
        if my_title:
            titles = Book.query.filter(Book.title.like(f"%{my_title}%")).all()
        else :
            titles = "rieng"
            # return render_template("partials/index.html", titres=titles)
    else :
        return render_template("pages/resultatsrecherche.html", titres=titles)
    return render_template("partials/index.html", titres=titles)

@app.route("/book_to_film/results", methods=['GET', 'POST'])
def search_adaptations():
    titles = ""
    if request.method == "POST":
        donnees = request.form
        print(donnees)
        my_title = donnees.get("title")
        if my_title:
            titles = Book.query.filter(Book.title.like(f"%{my_title}%")).all()
        else :
            # à tester/modifier
            titles = "rieng"
    else :
        return render_template("pages/resultatsrecherche.html", titres=titles)
    return render_template("pages/resultatsrecherche.html", titres=titles)


@app.route("/results", methods=['GET', 'POST'])
def results():
    titles = ""
    if request.method == "POST":
        donnees = request.form
        # print(donnees)
        my_title = donnees.get("title")
        if my_title:
            titles = Book.query.filter(Book.title.ilike(f"%{my_title}%")).all()
            # Si silence (la recherche de titre de livre ne donne rien) alors on checke chez les auteurs
            if len(titles) == 0:
                titles = Book.query.filter(Book.author.ilike(f"%{my_title}%")).all()
        else :
            titles = []
    else :
        return render_template("pages/resultatsrecherche.html", titres=titles)
    return render_template("pages/resultatsrecherche.html", titres=titles)

# ROUTE pour TESTER la TABLE DE RELATION
@app.route("/book_to_film/<string:id_book_>")
def check_adaptation(id_book_):
    # Créer une requête pour interroger directement la table de relation book_film
    stmt = select(film_book.c.id_film).where(film_book.c.id_book == id_book_)
    result = db.session.execute(stmt).fetchall()
    films = []
    for row in result:
        id_t = row[0]
        film = Film.query.filter_by(id=id_t).first()
        if film:
            films.append({
                "id_" : film.id,
                "title" : film.title,
                "director": film.director,
                "genres": film.genres, 
                "release_year": film.release_year, 
                "url_wikidata": film.url_wikidata, 
                "id_wikidata": film.id_wikidata,
                "color": notation_film(film.rating)
            })
        else :
            return "Aucun film trouvé pour ce livre", 404
    if films:
        # return render_template("pages/resultatsrecherche.html", titres_film=films)
        # return f"*{films[0].title} * {result}"
        return render_template("pages/resultats_adaptation.html", films=films)
    else:
        return "Aucun film trouvé pour ce livre", 404

# Fonction pour indiquer une couleur pour chaque film selon sa note présente dans la base de données
def notation_film(note_film):
    if note_film is None:  # Dans le cas où la note n'est pas renseignée
        return "gray"  # Couleur neutre pour films sans note
    
    if note_film <= 3.9:
        return "red"
    elif 4 <= note_film <= 6.9:
        return "orange"
    else:
        return "green"
    

@app.route("/random_book")
def random_book():
    book_count = Book.query.count()
    if book_count == 0:
        return jsonify({"error": "No books found"}), 404

    random_offset = random.randint(0, book_count - 1)
    random_book = Book.query.offset(random_offset).first()

    if random_book:
        return jsonify({
            "id": random_book.id,  # Add the book ID here
            "title": random_book.title,
            "author": random_book.author
        })
    else:
        return jsonify({"error": "No book found"}), 404

# ROUTE POUR AFFICHER LA LISTE DES LIVRES DE LA BASE DE DONNÉES
@app.route('/index-books')
def list_books():
    """Fonction qui permet d'afficher la liste des livres présents dans la base de données.

    Returns
    -------
    Retourne la liste des livres selon le template index-books.html
    """
    page = request.args.get('page', 1, type=int) # numéro de page à afficher, la liste des livres commence à la page 1 par défaut
    books_paginated = Book.query.paginate(page=page, per_page=app.config["BOOKS_PER_PAGE"], error_out=False)
    
    return render_template('partials/index-books.html', books=books_paginated)


# ROUTE POUR AFFICHER LA LISTE DES FILMS DE LA BASE DE DONNÉES
@app.route('/index-films')
def list_films():
    """Fonction qui permet d'afficher la liste des films présents dans la base de données.

    Returns
    -------
    Retourne la liste des films selon le template index-films.html

    """
    page = request.args.get('page', 1, type=int) # numéro de page à afficher, la liste des films commence à la page 1 par défaut
    films_paginated = Film.query.paginate(page=page, per_page=app.config["FILMS_PER_PAGE"], error_out=False)
    
    return render_template('partials/index-films.html', films=films_paginated)