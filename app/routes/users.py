from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify, Response
from app.models.adapte_moi import Film, Collection
from app.models.users import Users
from app.models.formulaires import AjoutUtilisateur, Connexion
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, login_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))

# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     flash('Vous devez être connecté pour accéder à cette page.', 'warning')
#     return redirect(url_for('login'))

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
    return render_template('partials/monprofil.html', films=films_dans_collection, collection_name=collection_name)

@app.route("/ajouter_collection/<string:film_id>")
@login_required
def ajouter_collection(film_id):
    film = Film.query.get(film_id)
    if film:
        nouvelle_collection = Collection(
            user_id=current_user.id,
            film_id=film.id,
            film_title=film.title,
            film_genre=film.genres
        )
        db.session.add(nouvelle_collection)
        db.session.commit()
        flash(f'Film "{film.title}" ajouté à votre collection.', 'success')
    else:
        flash('Film non trouvé.', 'error')
    return redirect(url_for('afficher_collection'))

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

    films = (
        db.session.query(Film)
        .join(Collection, Film.id == Collection.film_id)
        .filter(Collection.user_id == user_id)
        .all()
    )

    genres = [film.genres for film in films if film.genres]
    unique_genres = sorted(set(genres))
    counts = [genres.count(genre) for genre in unique_genres]

    axis.bar(unique_genres, counts, color='#EDA2A2')
    axis.set_title("Répartition des genres de films dans votre collection")
    axis.set_xlabel("Genre")
    axis.set_ylabel("Nombre de films")

    return fig
