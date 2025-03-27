from ..app import app, db

film_book = db.Table(
    "film_book",
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
        secondary=film_book, 
        backref=db.backref('books', lazy='dynamic')
        )

    def __repr__(self):
        return '<Book %r>' % (self.id)


class Film(db.Model):
    __tablename__ = "Film"
    collections = db.relationship('Collection', backref='film', lazy=True)

    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text)
    director = db.Column(db.Text)
    release_year = db.Column(db.Date)
    genres = db.Column(db.Text)
    rating = db.Column(db.Float)
    id_imdb = db.Column(db.Text)
    id_wikidata = db.Column(db.Text)
    url_wikidata = db.Column(db.Text)

    def __repr__(self):
        return '<Film %r>' % (self.id)
    
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, db.ForeignKey('users.id'), nullable=False)
    film_id = db.Column(db.Text, db.ForeignKey('Film.id'), nullable=False)
    film_title = db.Column(db.Text, nullable=False)
    # film = db.relationship('Film', backref=db.backref('collections', lazy=True))