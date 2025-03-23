from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort, jsonify
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
