from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort
from ..models.users import Users
from ..models.formulaires import AjoutUtilisateur


@app.route("/login")
def login():
    # return app/statics/test.pyredirect(url_for("index"))
    return render_template("partials/index.html")

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
            return redirect(url_for("/"))
        else:
            flash(",".join(donnees), "error")
            return render_template("partials/register.html", form=form)
    else :
        return render_template("partials/register.html", form=form)