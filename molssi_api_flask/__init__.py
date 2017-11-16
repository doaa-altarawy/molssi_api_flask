from flask import Flask, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from config import config
from flask_mongoengine import MongoEngine
from flask_mail import Mail
import os


mail = Mail()
db = MongoEngine()      # flask_mongoengine
cors = CORS()
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# For: @app.route("/api/v1/users")
# bootstrap = Bootstrap()





def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    print(app.config['APPLICATION_ROOT'])

    # init
    mail.init_app(app)
    db.init_app(app)
    cors.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

