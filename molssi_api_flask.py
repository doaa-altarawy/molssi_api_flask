from app import create_app, db
from werkzeug.contrib.profiler import ProfilerMiddleware
# from flask_migrate import Migrate, upgrade
import os
from app import logger


# Determine config settings from environment variables.
config_name = os.getenv('FLASK_CONFIG') or 'development'

# Setup logging levels
logger.setup_logging(config_name=config_name)

app = create_app(config_name)

# if app.config['TESTING']:
#     app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

# migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)  # , use_reloader=False)
