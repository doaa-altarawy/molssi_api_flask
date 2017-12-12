"""Flask app configuration
"""
import os


class BaseConfig:

    SETTINGS = "DEVELOP"
    # SETTINGS = "TESTING"
    # SETTINGS = "PRODUCTION"

    _basedir = os.path.abspath(os.path.dirname(__file__))
    APPLICATION_ROOT = os.path.join(_basedir, 'molssi_api_flask')
    STATIC_FOLDER = 'static'

    ADMINS = frozenset(['daltarawy@vt.edu'])
    SECRET_KEY = 'SecretKeyForSessionSigning'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
    DATABASE_CONNECT_OPTIONS = {}

    THREADS_PER_PAGE = 8

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "somethingimpossibletoguess"

    # email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Client-side config
    API_RESULTS_PER_PAGE = 5
    EXECLUDE_EMPTY_LIB = True
    
    # Jinia template
    REPLACE_NONE = '?'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WORDPRESS_DOMAIN = 'http://localhost:8888'
    API_DOMAIN = 'http://localhost:5000'
    MONGODB_SETTINGS = {
        'host': "mongodb://user:123@localhost:27017/resources_website",  # URI
        # 'host': "mongodb://user:123@ds127163.mlab.com:27163/resources_website",
        # 'db': 'project1',
        # 'host': 'localhost',
        # 'port': 12345,
        # 'username': 'ninja',
        # 'password': '123'
    }

class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WORDPRESS_DOMAIN = 'http://molssi.org'
    API_DOMAIN = 'http://molssi-api.herokuapp.com'
    MONGODB_SETTINGS = {
        'host': "mongodb://user:123@ds127163.mlab.com:27163/resources_website"
    }


class ProductionConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    WORDPRESS_DOMAIN = 'http://molssi.org'
    API_DOMAIN = 'http://api.molssi.org'
    MONGODB_SETTINGS = {
        'host': "mongodb://user:123@ds127163.mlab.com:27163/resources_website",
    }


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 'docker': DockerConfig,

    'default': DevelopmentConfig
}
