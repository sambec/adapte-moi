from ..app import app, db
from flask import render_template, request, flash, redirect, url_for, abort, Flask, jsonify, render_template
from collections import Counter
# from ..models.formulaires import Recherche

@app.route("/login")
def login():
    # return app/statics/test.pyredirect(url_for("index"))
    return render_template("partials/index.html")

@app.route('/user/<int:user_id>/radar-data')
def radar_data(user_id):
    user_collections = Collection.query.filter_by(user_id=user_id).all()
    genres_list = []

    for collection in user_collections:
        if collection.film.genres:
            genres_list.extend(collection.film.genres.split(", "))

    genre_counts = Counter(genres_list)

    return jsonify({
        "labels": list(genre_counts.keys()),
        "data": list(genre_counts.values())
    })

@app.route('/user/<int:user_id>/radar')
def radar_chart(user_id):
    return render_template('radar.html', user_id=user_id)
