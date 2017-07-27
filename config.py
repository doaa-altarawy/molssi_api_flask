import os
_basedir = os.path.abspath(os.path.dirname(__file__))

IS_DEVELOP = True

APPLICATION_ROOT = os.path.join(_basedir, 'molssi_api_flask')
STATIC_FOLDER = 'static'

# Database:
DB_NAME = 'resources_website'
DB_HOST = 'localhost'
DB_PORT = 27017

if IS_DEVELOP:
    DEBUG = True
    TESTING = True
    WORDPRESS_DOMAIN = 'http://localhost:8888'
    API_DOMAIN = 'http://localhost:5000'
else:
    DEBUG = True
    TESTING = False
    WORDPRESS_DOMAIN = 'http://molssi.org'
    API_DOMAIN = 'http://api.molssi.org'

ADMINS = frozenset(['daltarawy@vt.edu'])
SECRET_KEY = 'SecretKeyForSessionSigning'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"
