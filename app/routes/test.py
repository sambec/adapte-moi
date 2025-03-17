from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, request
from sqlalchemy import or_
from ..models.adapte_moi import Film, Book
# from ..models.formulaires import Recherche
# from ..utils.transformations import nettoyage_string_to_int, clean_arg

@app.route("/test_book")
def test_book():
    books = []
    for book in Book.query.all():
        books.append(book.title)
    return render_template("pages/test.html", livres=books)

@app.route("/books/<string:book_name>")
def get_book(book_name):
    book = Book.query.filter_by(title=book_name).first()
    if book:
        # return render_template("pages/test.html", livre=book.title, auteur=book.author)
        return render_template("pages/livre.html", livre=book.title, auteur=book.author)
    else:
        return "Livre non trouvé", 404

@app.route("/author/<string:author_name>")
def get_author(author_name):
    author = Book.query.filter_by(author=author_name).first()
    if author:
        # return render_template("pages/test.html", livre=book.title, auteur=book.author)
        return render_template("pages/auteur.html", auteur=author.author)
    else:
        return "auteur non trouvé", 404
    
@app.route("/recherche", methods=['GET', 'POST'])
def recheche():
    titles = ""
    if request.method == "POST":
        donnees = request.form
        print(donnees)
        my_title = donnees.get("title")
        if my_title:
            titles = Book.query.filter(Book.title.like(f"%{my_title}%")).all()
        else :
            titles = "rieng"
    else :
        return render_template("pages/test.html", titres=titles)
    return render_template("pages/index.html", titres=titles)

@app.route("/test_movie")
def test_movie():
    movies = []
    for movie in Film.query.all():
        movies.append(movie.title)
    return render_template("pages/test.html", films=movies)



