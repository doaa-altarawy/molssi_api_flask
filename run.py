#!venv/bin/python

from molssi_api_flask import create_app, db
# from flask_migrate import Migrate, upgrade
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# migrate = Migrate(app, db)

app.run()
