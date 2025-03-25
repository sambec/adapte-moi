from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort, jsonify
from sqlalchemy import or_, select
from ..models.adapte_moi import Film, Book, film_book
import io
import random
from flask import Flask, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from wordcloud import WordCloud #il faudra mettre tout ça dans un pip freeze:: pip install flask flask-sqlalchemy matplotlib wordcloud

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

# Route pour afficher le graphique
@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# Fonction qui génère le graphique
def create_figure():

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    # Récupération des données depuis la base SQL
    films = Film.query.order_by(Film.release_year).all()
    
    # Extraction des données pour l'axe X (années) et Y (nombre de livres publiés)
    years = [Film.release_year for Film in films if Film.release_year]
    unique_years = sorted(set(years))
    counts = [years.count(year) for year in unique_years]

    # Création du graphique
    axis.plot(unique_years, counts, marker='o', linestyle='-', color='#EDA2A2')
    axis.set_title("Nombre de films adaptés des livres par années")
    axis.set_xlabel("Année")
    axis.set_ylabel("Nombre de films")

    return fig

@app.route("/about")
def about():
    return render_template("partials/about.html", title="À propos")

# -------------------- AUTHENTIFICATION --------------------

# 🎨 Définition des couleurs personnalisées
COLOR_PALETTE = ["#EDA2A2", "#9AC9C1", "#FEEBB3", "#F28B66", "#4D7F96"]

def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Fonction pour appliquer les couleurs personnalisées."""
    return random.choice(COLOR_PALETTE)

# Route pour générer le nuage de mots
@app.route('/wordcloud.png')
def wordcloud():
    fig = create_wordcloud()
    output = io.BytesIO()
    fig.savefig(output, format='png', bbox_inches='tight')
    output.seek(0)
    return Response(output.getvalue(), mimetype='image/png')

# Fonction pour créer le nuage de mots
def create_wordcloud():
    films = Film.query.all()
    text = " ".join([film.genres for film in films if film.genres])  # Récupération des genres
    
    wordcloud = WordCloud(
        width=800, height=400,
        background_color="white",
        colormap=None,  # Désactivation du colormap par défaut
        collocations=False,
        color_func=custom_color_func  # Appliquer les couleurs personnalisées
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")  # Supprimer les axes
    return fig
