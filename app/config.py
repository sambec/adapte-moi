import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config():
    DEBUG = os.environ.get("DEBUG")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'adapte_moi.sqlite')
    SQLALCHEMY_ECHO=os.environ.get("SQLALCHEMY_ECHO")
    BOOKS_PER_PAGE = int(os.environ.get("BOOKS_PER_PAGE"))
    FILMS_PER_PAGE = int(os.environ.get("FILMS_PER_PAGE"))
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLE = os.environ.get("WTF_CSRF_ENABLE")