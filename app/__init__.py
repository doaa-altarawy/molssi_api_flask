from flask import Flask
from flask_cors import CORS, cross_origin
from config import config
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from template_filters import replace_empty
from flask_admin import Admin
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension


mail = Mail()
db = MongoEngine()      # flask_mongoengine
cors = CORS()
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# For: @app.route("/api/v1/users")
bootstrap = Bootstrap()
app_admin = Admin(name='MolSSI CMS Software DB Admin', template_mode='bootstrap3',
                  base_template='admin/custom_base.html')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'   # endpoint name for the login view

toolbar = DebugToolbarExtension()


def create_app(config_name):
    """Flask app factory pattern
       separately creating the extensions and later initializing"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    print('APPLICATION_ROOT:', app.config['APPLICATION_ROOT'])

    # init
    mail.init_app(app)
    db.init_app(app)
    cors.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    app_admin.init_app(app)
    # To avoid circular import
    from app.admin import add_admin_views
    add_admin_views()
    toolbar.init_app(app)

    # jinja template
    app.jinja_env.filters['empty'] = replace_empty

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

