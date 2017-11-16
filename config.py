"""Flask app configuration
"""

import os


SETTINGS = "DEVELOP"
# SETTINGS = "TESTING"
# SETTINGS = "PRODUCTION"

_basedir = os.path.abspath(os.path.dirname(__file__))
APPLICATION_ROOT = os.path.join(_basedir, 'molssi_api_flask')
STATIC_FOLDER = 'static'


if SETTINGS == "DEVELOP":
    DEBUG = True
    TESTING = False
    WORDPRESS_DOMAIN = 'http://localhost:8888'
    API_DOMAIN = 'http://localhost:5000'
    MONGODB_SETTINGS = {
        'host': "mongodb://user:123@localhost:27017/resources_website",  # URI
        # 'db': 'project1',
        # 'host': 'localhost',
        # 'port': 12345,
        # 'username': 'ninja',
        # 'password': '123'
    }

elif SETTINGS == "TESTING":  # (fake pass)
    DEBUG = True
    TESTING = True
    WORDPRESS_DOMAIN = 'http://molssi.org'
    API_DOMAIN = 'http://molssi-api.herokuapp.com'
    MONGODB_SETTINGS = {
        'host': "mongodb://user:123@ds127163.mlab.com:27163/resources_website"
    }

elif SETTINGS == "PRODUCTION":   # (fake pass)
    DEBUG = True
    TESTING = False
    WORDPRESS_DOMAIN = 'http://molssi.org'
    API_DOMAIN = 'http://api.molssi.org'
    MONGODB_SETTINGS = {
        'host': "mongodb://user:123@ds127163.mlab.com:27163/resources_website",
    }


ADMINS = frozenset(['daltarawy@vt.edu'])
SECRET_KEY = 'SecretKeyForSessionSigning'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"
