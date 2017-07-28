import os


SETTINGS = "DEVELOP"    # "TESTING", "PRODUCTION"

_basedir = os.path.abspath(os.path.dirname(__file__))
APPLICATION_ROOT = os.path.join(_basedir, 'molssi_api_flask')
STATIC_FOLDER = 'static'


if SETTINGS == "DEVELOP":
    DEBUG = True
    TESTING = True
    WORDPRESS_DOMAIN = 'http://localhost:8888'
    API_DOMAIN = 'http://localhost:5000'
    DB_URI = "mongodb://ninja:fakePass@localhost:27017/resources_website"

elif SETTINGS == "TESTING":  # (fake pass)
    DEBUG = True
    TESTING = False
    WORDPRESS_DOMAIN = 'http://molssi.org'
    API_DOMAIN = 'http://molssi-api.herokuapp.com'
    DB_URI = "mongodb://ninja:fakePass@ds127173.mlab.com:27173/heroku_rzz9knz9"

elif SETTINGS == "PRODUCTION":   # (fake pass)
    DEBUG = True
    TESTING = False
    WORDPRESS_DOMAIN = 'http://molssi.org'
    API_DOMAIN = 'http://api.molssi.org'
    DB_URI = "mongodb://ninja:fakePass@ds127173.mlab.com:27173/heroku_rzz9knz9"


ADMINS = frozenset(['daltarawy@vt.edu'])
SECRET_KEY = 'SecretKeyForSessionSigning'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"
