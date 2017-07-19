from flask import Blueprint, request, render_template, flash, g, session, \
                    redirect, url_for, abort, jsonify, send_from_directory,\
                    current_app
from molssi_api_flask.core.repository import *
from flask_jsonpify import jsonpify
import os
import json


mod = Blueprint('core', __name__)

@mod.route('/')
def index():
    repository = Repository()
    return (render_template('core/index.html', resources=repository.getResources()))


@mod.route('/resources_website')
def resources_website():

    return render_template('wordpress_page.html',
            WORDPRESS_DOMAIN = current_app.config['WORDPRESS_DOMAIN'],
            API_DOMAIN = current_app.config['API_DOMAIN']
        )


@mod.route('/test')
def test():
    # return json.dumps({'msg': "Hello from MolSSI api"})
    return jsonpify({'msg': 'Hello from MolSSI api jsonpify'})


@mod.route('/contact')
def contact():

    json_url = os.path.join(current_app.config['APPLICATION_ROOT'], 'static', 'data',
                            'test.json')
    print(json_url)
    # data = json.load(open(json_url))

    with mod.open_resource(json_url) as f:
      data = json.load(f)

    return jsonify(data)

    # For JSONP:
    # return jsonpify({
    #               'name': 'Doaa Altarawy',
    #               'info': 'Research Scientist at MolSSI'
    #               })
