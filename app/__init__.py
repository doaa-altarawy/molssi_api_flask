from flask import Flask
from flask_cors import CORS, cross_origin
from config import config
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from .template_filters import replace_empty
from flask_admin import Admin
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_moment import Moment
from . import logger
import logging
from flask_ckeditor import CKEditor


mail = Mail()
db = MongoEngine()
cors = CORS()
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# For: @app.route("/api/v1/users")
bootstrap = Bootstrap()
app_admin = Admin(name='MolSSI Molecular Software DB Admin', template_mode='bootstrap3',
                  base_template='admin/custom_base.html')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'   # endpoint name for the login view
moment = Moment()
toolbar = DebugToolbarExtension()
ckeditor = CKEditor()


def create_app(config_name):
    """Flask app factory pattern
       separately creating the extensions and later initializing"""

    # Setup logging levels
    logger.setup_logging(config_name=config_name)

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    logging.info('Creating app with config {}'.format(config_name))
    logging.info('Testing is {}'.format(app.config['TESTING']))

    # init
    mail.init_app(app)
    db.init_app(app)
    cors.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    # toolbar.init_app(app)
    ckeditor.init_app(app)

    # jinja template
    app.jinja_env.filters['empty'] = replace_empty

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # create user roles
    from .models.users import update_roles
    update_roles()

    # To avoid circular import
    from app.admin import add_admin_views
    add_admin_views()

    # Then init the app
    app_admin.init_app(app)

    return app

