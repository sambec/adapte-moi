from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from ..models.users import Users
from ..models.formulaires import AjoutUtilisateur, Connexion
from flask_login import login_user, current_user, logout_user


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

@app.route("/utilisateurs/profil", methods=["POST", "GET"])
def profil():
    return render_template("partials/monprofil.html")