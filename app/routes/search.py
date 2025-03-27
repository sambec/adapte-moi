from ..app import app, db
from flask import render_template, request, jsonify
from sqlalchemy import select
from ..models.adapte_moi import Film, Book, film_book
import random


# ROUTE POUR AFFICHER LES RÉSULTATS DE LA RECHERCHE
@app.route("/results", methods=['GET', 'POST'])
def results():
    """Fonction qui permet d'afficher les résultats de la recherche effectuée par l'utilisateur à partir de la page d'accueil.

    Returns
    -------
    Retourne les résultats de la recherche selon le template resultatsrecherche.html
    """
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


# ROUTE POUR AFFICHER LES ADAPTATIONS D'UN LIVRE
@app.route("/book_to_film/<string:id_book_>")
def check_adaptation(id_book_):
    """Fonction qui permet de vérifier les adaptations d'un livre en film.

    Parameters
    ----------
        id_book: str, required
            L'identifiant du livre

    Returns
    -------
        Retourne les adaptations cinématographiques liés à l'identifiant d'un livre.
    """
    # Créer une requête pour interroger directement la table de relation book_film
    stmt = select(film_book.c.id_film).where(film_book.c.id_book == id_book_)
    result = db.session.execute(stmt).fetchall()
    films = []
    for row in result:
        id_t = row[0]
        film = Film.query.filter_by(id=id_t).first()
        if film:
            films.append({
                "title" : film.title,
                "director": film.director,
                "genres": film.genres, 
                "release_year": film.release_year, 
                "url_wikidata": film.url_wikidata, 
                "id_wikidata": film.id_wikidata,
                "color": notation_film(film.rating)
            })
    if films:
        return render_template("pages/resultats_adaptation.html", films=films)
    else:
        return "Aucun film trouvé pour ce livre", 404

def notation_film(note_film):
    """Fonction qui permet d'associer une couleur pour chaque film selon les données de notation présentes dans la base de données.

    Parameters
    ----------
        note_film : float, required 
            Paramètre requis pour la fonction, il est nécessaire de renseigner la note d'un film pour utiliser cette fonction.

    Returns
    -------
        La fonction retourne nécessairement une couleur, si la note d'un film n'est pas renseignée la couleur sera grise.
    """
    if note_film is None:
        return "gray"
    
    if note_film <= 3.9:
        return "red"
    elif 4 <= note_film <= 6.9:
        return "orange"
    else:
        return "green"


# ROUTE POUR AFFICHER LES ADAPTATIONS D'UN LIVRE À PARTIR DE LA ROUTE /book_to_film/<string:id_book_>
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


# ROUTE POUR AFFICHER UN LIVRE DE FAÇON ALÉATOIRE
@app.route("/random_book")
def random_book():
    """Fonction qui permet d'afficher un livre de façon aléatoire.

    Returns
    -------
    L'identifiant du livre avec son titre et son auteur de façon aléatoire, sinon retourne une erreur 404 "No book found".
    """
    book_count = Book.query.count()
    if book_count == 0:
        return jsonify({"error": "No books found"}), 404

    random_offset = random.randint(0, book_count - 1)
    random_book = Book.query.offset(random_offset).first()

    if random_book:
        return jsonify({
            "id": random_book.id,
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