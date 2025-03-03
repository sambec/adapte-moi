from ..app import app, db
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import or_
from ..models.adapte_moi import Film, Book
# from ..models.formulaires import Recherche
# from ..utils.transformations import nettoyage_string_to_int, clean_arg

@app.route("/test_book")
def test_book():
    books = []
    for book in Book.query.all():
        books.append(book.title)
    return render_template("pages/index.html", livres=books)

@app.route("/test_movie")
def test_movie():
    movies = []
    for movie in Film.query.all():
        movies.append(movie.title)
    return render_template("pages/index.html", films=movies)



