from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify, request
from sqlalchemy import or_, select
from ..models.adapte_moi import Film, Book, film_book
# from ..models.formulaires import Recherche
# from ..utils.transformations import nettoyage_string_to_int, clean_arg

# @app.route("/test_book")
# def test_book():
#     books = []
#     for book in Book.query.all():
#         books.append(book.title)
#     return render_template("pages/test.html", livres=books)

@app.route("/book/<string:book_name>")
def get_book(book_name):
    book = Book.query.filter_by(title=book_name).first()
    if book:
        return render_template("pages/livre.html", livre=book.title, auteur=book.author)
    else:
        return "Livre non trouvé", 404

@app.route("/author/<string:author_name>")
def get_author(author_name):
    author = Book.query.filter_by(author=author_name).first()
    if author:
        return render_template("pages/auteur.html", auteur=author.author)
    else:
        return "auteur non trouvé", 404
    
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

@app.route("/results", methods=['GET', 'POST'])
def results():
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

# ROUTE pour TESTER la TABLE DE RELATION
@app.route("/book_to_film/<string:id_book_>")
def check_adaptation(id_book_):
    # Créer une requête pour interroger directement la table de relation book_film
    stmt = select(film_book.c.id_film).where(film_book.c.id_book == id_book_)
    result = db.session.execute(stmt).fetchall()
    films = []
    for i in range(len(result)):
        # print(result[i][0])
        id_t = result[i][0]
        films.append(Film.query.filter_by(id=id_t).first())
    if result:
        # return render_template("pages/resultatsrecherche.html", titres_film=films)
        return f"*{films[0].title} * {result}"
    else:
        return "Aucun film trouvé pour ce livre", 404

# @app.route("/test_movie")
# def test_movie():
#     movies = []
#     for movie in Film.query.all():
#         movies.append(movie.title)
#     return render_template("pages/test.html", films=movies)
