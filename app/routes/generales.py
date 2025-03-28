from ..app import app, db
from flask import render_template, Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import io
import random
from wordcloud import WordCloud 
from ..models.adapte_moi import Film, Book, film_book
from flask_login import current_user

# from ..models.formulaires import Recherche

# ROUTE POUR LA GESTION DES ERREURS
@app.errorhandler(404)
def page_not_found(error):
    """Fonction qui permet de gérer les erreurs 404 liées à une page non trouvé.

    Paramaters
    ----------
        error (_type_): _description_

    Returns
    -------
        Si la page n'est pas trouvée, retourne le template 404.html.
    """
    return render_template('partials/404.html'), 404

# ROUTES POUR LA REDIRECTION VERS LA PAGE D'ACCUEIL
@app.route("/")

@app.route("/accueil")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        print(f'Utilisateur {current_user.id} \({current_user.pseudo}\) est connecté.')
    else:
        print(f'(Aucun utilisateur n\'est connecté.')
    return render_template("partials/index.html")

# ROUTE POUR LA PAGE À PROPOS
@app.route("/about")
def about():
    return render_template("partials/about.html")


# ROUTE POUR DE LA PAGE SUR LA PRÉSENTATION DU PROCESSUS D'ADAPTATION
@app.route("/adaptation")
@app.route("/adaptation.html")
def adaptation():
    return render_template("partials/adaptation.html")

# ROUTE POUR EXPLORER LES COLLECTIONS
@app.route("/top")
@app.route("/top.html")
def top():
    return render_template("partials/top.html")


# ROUTE POUR AFFICHER UN GRAPHIQUE
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


# -------------------- AUTHENTIFICATION --------------------

# 🎨 Définition des couleurs personnalisées
COLOR_PALETTE = ["#EDA2A2", "#9AC9C1", "#FEEBB3", "#F28B66", "#4D7F96"]

def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """Fonction pour appliquer les couleurs personnalisées

    Returns
    -------
        _type_: _description_
    """
    return random.choice(COLOR_PALETTE)


# ROUTE POUR GÉNÉRER UN GRAPHIQUE EN NUAGE DE MOTS
@app.route('/wordcloud.png')
def wordcloud():
    """_summary_

    Returns:
        _type_: _description_
    """
    fig = create_wordcloud()
    output = io.BytesIO()
    fig.savefig(output, format='png', bbox_inches='tight')
    output.seek(0)
    return Response(output.getvalue(), mimetype='image/png')

# Fonction pour créer le nuage de mots
def create_wordcloud():
    """_summary_

    Returns:
        _type_: _description_
    """
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



