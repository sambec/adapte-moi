from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager
import unicodedata
import re

app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='statics')
app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)

def slugify(value):
    """
    Convert to ASCII, convert to lowercase, remove non-word characters
    (alphanumerics and underscores), and join them with hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

app.jinja_env.filters['slugify'] = slugify

from .routes import generales, users, search
