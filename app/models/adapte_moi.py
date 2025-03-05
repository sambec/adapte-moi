from app import app, db

book_film = db.Table(
    "book_film",
    db.Column('id_film', db.Text, db.ForeignKey('Film.id')),
    db.Column('id_book', db.Text, db.ForeignKey('Book.id'))
)

class Book(db.Model):
    __tablename__ = "Book"

    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    publication_year = db.Column(db.Date)
    curriculum = db.Column(db.Text)
    educational_level = db.Column(db.Text)
    main_theme = db.Column(db.Text)
    secondary_theme = db.Column(db.Text)
    issue = db.Column(db.Text)
    id_wikidata = db.Column(db.Text)
    url_wikidata = db.Column(db.Text)

    film = db.relationship(
        'Film', 
        secondary=book_film, 
        backref='film'
        )

    def __repr__(self):
        return '<Book %r>' % (self.id)


class Film(db.Model):
    __tablename__ = "Film"

    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text)
    director = db.Column(db.Text)
    release_year = db.Column(db.Date)
    genres = db.Column(db.Text)
    rating = db.Column(db.Real)
    id_imdb = db.Column(db.Text)
    id_wikidata = db.Column(db.Text)
    url_wikidata = db.Column(db.Text)

    def __repr__(self):
        return '<Film %r>' % (self.id)