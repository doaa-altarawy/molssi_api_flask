from flask import Flask, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import molssi_api_flask.core.mongo_database as db


app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# For: @app.route("/api/v1/users")

app.config.from_object('config')
print(app.config['APPLICATION_ROOT'])

#  MongoDB connection
db.get_connection(host=app.config['DB_URI'])

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

from molssi_api_flask.core.views import mod as core
app.register_blueprint(core)

#app.register_blueprint(core, url_prefix='/api')

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)
