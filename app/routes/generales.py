from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort

# from ..models.formulaires import Recherche


@app.route("/")
def accueil():
    return redirect(url_for("index"))




