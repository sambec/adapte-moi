from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort

# from ..models.formulaires import Recherche

@app.route("/login")
def login():
    # return app/statics/test.pyredirect(url_for("index"))
    return render_template("partials/index.html")
