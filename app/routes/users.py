from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort, session
from ..models.users import Users
from ..models.adapte_moi import Film, Collection
from ..models.formulaires import AjoutUtilisateur, Connexion
from flask_login import login_user, current_user, logout_user, login_required


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
            print("Hop, un nouvel utilisateur", "success")
            # return redirect(url_for("accueil"))
            return "bravo ! nouvel utilisateur !"
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
            print("Connexion effectuée !!!")
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("home"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
            print("Connexion RATEE")
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
    # Récupérer les films de la collection de l'utilisateur connecté
    films_dans_collection = (
        db.session.query(Film)
        .join(Collection, Film.id == Collection.film_id)
        .filter(Collection.user_id == current_user.id)
        .all()
    )
    return render_template('partials/monprofil.html', films=films_dans_collection)


@app.route("/ajouter_collection/<string:film_id>")
@login_required
def ajouter_collection(film_id):
    film = Film.query.get(film_id)

    if film:
        nouvelle_collection = Collection(
            user_id=current_user.id, 
            film_id=film.id,
            film_title=film.title
        )
        db.session.add(nouvelle_collection)
        db.session.commit()
        flash(f'Film "{film.title}" ajouté à votre collection.', 'success')
        print(f'Film "{film.title}" ajouté à votre collection.', 'success')
    else:
        flash('Film non trouvé.', 'error')
        print('Film non trouvé.', 'error')
    return redirect(url_for('afficher_collection'))