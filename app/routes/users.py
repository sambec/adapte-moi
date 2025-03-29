from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify, Response
from app.models.adapte_moi import Film, Collection
from app.models.users import Users
from app.models.formulaires import AjoutUtilisateur, Connexion
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, login_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import numpy as np

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#////////////////////Pour la Connection////////////////////



@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Vous devez être connecté pour accéder à cette page.', 'warning')
    # print("non")
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = AjoutUtilisateur()
    if form.validate_on_submit():
        statut, donnees = Users.ajout(
            pseudo=request.form.get("pseudo", None),
            password=request.form.get("password", None)
        )
        if statut is True:
            flash("Hop, un nouvel utilisateur", "success")
            return redirect(url_for("home"))
        else:
            flash(",".join(donnees), "error")
    return render_template("partials/register.html", form=form)

@app.route("/utilisateurs/connexion", methods=["GET", "POST"])
def login():
    form = Connexion()
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté", "info")
        return redirect(url_for("home"))
    if form.validate_on_submit():
        utilisateur = Users.identification(
            pseudo=request.form.get("pseudo", None),
            password=request.form.get("password", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("home"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
    return render_template("partials/login.html", form=form)

@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated:
        logout_user()
    flash("Vous êtes déconnecté", "info")
    return redirect(url_for("home"))

#////////////////////Pour la recommandation dans la page MONRPOFIL selon les genres de la Collection////////////////////


def get_recommendation(user_id):
    # Récupération des films de la collection de l'utilisateur
    films_dans_collection = (
        db.session.query(Film)
        .join(Collection, Film.id == Collection.film_id)
        .filter(Collection.user_id == user_id)
        .all()
    )

    # Extraction des genres
    genres = [film.genres for film in films_dans_collection if film.genres]
    unique_genres = sorted(set(genres))
    counts = [genres.count(genre) for genre in unique_genres]

    # Identifier le genre le plus fréquent
    if counts:
        most_frequent_genre = unique_genres[counts.index(max(counts))]
    else:
        return None

    # Sélectionner un film aléatoire du genre le plus fréquent
    recommended_film = (
        db.session.query(Film)
        .filter(Film.genres == most_frequent_genre)
        .order_by(db.func.random())
        .first()
    )

    return recommended_film

#////////////////////Pour la gestion de la Collection////////////////////

@app.route('/profil')
@app.route('/collection')
@login_required
def afficher_collection():
    films_dans_collection = (
        db.session.query(Film)
        .join(Collection, Film.id == Collection.film_id)
        .filter(Collection.user_id == current_user.id)
        .all()
    )
    collection = Collection.query.filter_by(user_id=current_user.id).first()
    collection_name = collection.name if collection else 'Ma collection de films'

    # Obtenir une recommandation basée sur les genres de films dans la collection
    recommandation = get_recommendation(current_user.id)

    return render_template('partials/monprofil.html', films=films_dans_collection, collection_name=collection_name, recommandation=recommandation)

#----------------Ajouter un film dans la collection---------------


@app.route("/ajouter_collection/<string:film_id>")
@login_required
def ajouter_collection(film_id):
    if not current_user.is_authenticated:
        flash("Vous devez être connecté pour ajouter un film à votre collection.", "warning")
        return redirect(url_for('login'))
    
    film = Film.query.get(film_id)

    if not film:
        flash('Film non trouvé.', 'error')
        return redirect(url_for('afficher_collection'))

    # Vérifier si le film est déjà dans la collection de l'utilisateur
    existe_deja = Collection.query.filter_by(user_id=current_user.id, film_id=film.id).first()
    if existe_deja:
        flash(f'Le film "{film.title}" est déjà dans votre collection.', 'warning')
    else:
        nouvelle_collection = Collection(
            user_id=current_user.id,
            film_id=film.id,
            film_title=film.title,
            film_genre=film.genres
        )
        db.session.add(nouvelle_collection)
        db.session.commit()
        flash(f'Film "{film.title}" ajouté à votre collection.', 'success')

    return redirect(url_for('afficher_collection'))


#----------------Renommer la collection---------------


@app.route('/renommer_collection', methods=['POST'])
@login_required
def renommer_collection():
    data = request.get_json()
    new_name = data.get('name')
    collection = Collection.query.filter_by(user_id=current_user.id).first()
    if collection:
        collection.name = new_name
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})

#----------------Supprimer un film de la collection---------------


@app.route('/supprimer_collection/<string:film_id>', methods=['POST'])
@login_required
def supprimer_collection(film_id):
    collection_a_supprimer = Collection.query.filter_by(
        user_id=current_user.id, film_id=film_id).first()
    if collection_a_supprimer:
        db.session.delete(collection_a_supprimer)
        db.session.commit()
        flash(f'Film supprimé de votre collection.', 'success')
    else:
        flash('Film non trouvé dans votre collection.', 'error')
    return redirect(url_for('afficher_collection'))




#////////////////////LES DATAVIZ de la page MONPROFIL////////////////////



#----------------L'histogramme selon les genres dans la collection---------------

@app.route('/genre_plot.png')
@login_required
def genre_plot_png():
    fig = create_genre_figure(current_user.id)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_genre_figure(user_id):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    # Récupération des données depuis la base SQL
    films = (
        db.session.query(Film)
        .join(Collection, Film.id == Collection.film_id)
        .filter(Collection.user_id == user_id)
        .all()
    )

    # Extraction des données pour les genres
    genres = [film.genres for film in films if film.genres]
    unique_genres = sorted(set(genres))
    counts = [genres.count(genre) for genre in unique_genres]

    axis.bar(unique_genres, counts, color='#EDA2A2')
    axis.set_title("Répartition des genres de films dans votre collection")
    axis.set_xlabel("Genre")
    axis.set_ylabel("Nombre de films")

    return fig

#----------------Le graphique en radar selon les genres dans la collection---------------

@app.route('/genre_radar.png')
@login_required
def genre_radar_png():
    fig = create_genre_radar(current_user.id)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_genre_radar(user_id):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1, polar=True)

    # Récupération des données depuis la base SQL
    films = (
        db.session.query(Film)
        .join(Collection, Film.id == Collection.film_id)
        .filter(Collection.user_id == user_id)
        .all()
    )

    # Extraction des données pour les genres
    genres = [film.genres for film in films if film.genres]
    unique_genres = sorted(set(genres))
    counts = [genres.count(genre) for genre in unique_genres]

    # Ajout des genres manquants pour avoir un graphique complet
    num_vars = len(unique_genres)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    counts += counts[:1]
    angles += angles[:1]

    # Création du graphique en radar
    axis.fill(angles, counts, color='#EDA2A2', alpha=0.25)
    axis.plot(angles, counts, color='#EDA2A2', linewidth=2)
    axis.set_theta_offset(np.pi / 2)
    axis.set_theta_direction(-1)
    axis.set_thetagrids(np.degrees(angles[:-1]), unique_genres)
    axis.set_title("Répartition des genres de films dans votre collection")

    return fig

