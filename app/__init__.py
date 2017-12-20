from flask import Flask
from flask_cors import CORS, cross_origin
from config import config
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from template_filters import replace_empty
from flask_admin import Admin


mail = Mail()
db = MongoEngine()      # flask_mongoengine
cors = CORS()
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# For: @app.route("/api/v1/users")
bootstrap = Bootstrap()
admin = Admin()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    print('APPLICATION_ROOT:', app.config['APPLICATION_ROOT'])

    # init
    mail.init_app(app)
    db.init_app(app)
    cors.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)
    # To avoid circular import
    from app.main.admin import add_admin_views
    add_admin_views()

    # jinja template
    app.jinja_env.filters['empty'] = replace_empty

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

