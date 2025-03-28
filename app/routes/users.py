from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, jsonify, abort, session
from ..models.users import Users
from ..models.adapte_moi import Film, Collection
from ..models.formulaires import AjoutUtilisateur, Connexion
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

# @app.route("/login")
# def login():
#     # return app/statics/test.pyredirect(url_for("index"))
#     print("log")
#     return render_template("partials/index.html")

# REGISTER / ENREGISTREMENT
@app.route("/register", methods=["GET", "POST"])
def register():
    # FORMULAIRE pour add un user : voir formulaire.py, classe AjoutUtilisateur
    form = AjoutUtilisateur()

    # Si validation via méthod post 
    if form.validate_on_submit():
        statut, donnees = Users.ajout(
            pseudo=request.form.get("pseudo", None), 
            password=request.form.get("password", None)
        )
        if statut is True:
            flash("Hop, un nouvel utilisateur", "success")
            # print("Hop, un nouvel utilisateur", "success")
            return redirect(url_for("home"))
        else:
            flash(",".join(donnees), "error")
            print("existe déjà")
            return render_template("partials/register.html", form=form)
    else :
        return render_template("partials/register.html", form=form)

# CONNEXION
# @app.route("/login", methods=["GET","POST"])
# @app.route("/connexion", methods=["GET","POST"])
@app.route("/utilisateurs/connexion", methods=["GET","POST"])
def login():
    form = Connexion()

    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté", "info")
        # print("connexion")
        # return redirect(url_for("home"))

    if form.validate_on_submit():
        utilisateur = Users.identification(
            pseudo=request.form.get("pseudo", None),
            password=request.form.get("password", None)
        )
        if utilisateur:
            # print("Connexion effectuée !!!")
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("home"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
            # print("Connexion RATEE")
            return render_template("partials/login.html", form=form)

    else:
        return render_template("partials/login.html", form=form)

@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté", "info")
    return redirect(url_for("home"))


login.login_view = 'connexion'

# GESTION COLLECTION DE FILMS
@app.route('/profil')
@app.route('/collection')
@login_required
def afficher_collection():
    # Récupère les films de la collection de l'utilisateur connecté
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
        print(f'Film "{film.title}" ajouté à votre collection.', 'success')
    else:
        flash('Film non trouvé.', 'error')
        print('Film non trouvé.', 'error')
    return redirect(url_for('afficher_collection'))

@app.route('/renommer_collection', methods=['POST'])
@login_required
def renommer_collection():
    data = request.get_json()
    new_name = data.get('name')

    # Mettre à jour le nom de la collection dans la base de données
    # Assurez-vous de mettre à jour la bonne collection pour l'utilisateur connecté
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

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Vous devez être connecté pour accéder à cette page.', 'warning')
    # print("non")
    return redirect(url_for('login'))
# @app.route('/user/<int:user_id>/radar-data')
# def radar_data(user_id):
#     user_collections = Collection.query.filter_by(user_id=user_id).all()
#     genres_list = []

#     for collection in user_collections:
#         if collection.film.genres:
#             genres_list.extend(collection.film.genres.split(", "))

#     genre_counts = Counter(genres_list)

#     return jsonify({
#         "labels": list(genre_counts.keys()),
#         "data": list(genre_counts.values())
#     })

# @app.route('/user/<int:user_id>/radar')
# def radar_chart(user_id):
#     return render_template('radar.html', user_id=user_id)
