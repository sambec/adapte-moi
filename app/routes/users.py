# from ..app import app, db
# from flask import render_template, request, flash, redirect, url_for, abort

# from ..models.formulaires import Recherche


# @app.route("/")
# def home():
#     return render_template('index.html')

# # -------------------- UTILISATEURS --------------------

# @app.route("/utilisateurs")
# def utilisateurs():
#     utilisateurs = db.session.execute("SELECT id, name, email FROM user").fetchall()
#     return render_template("pages/utilisateurs.html", utilisateurs=utilisateurs, sous_titre="Tous les utilisateurs")


# @app.route("/utilisateur/<int:id>")
# def utilisateur_specifique(id):
#     utilisateur = db.session.execute("SELECT id, name, email FROM user WHERE id = :id", {"id": id}).fetchone()
#     if not utilisateur:
#         return render_template("pages/404.html"), 404
#     return render_template("pages/utilisateur.html", utilisateur=utilisateur, sous_titre=utilisateur.name)

