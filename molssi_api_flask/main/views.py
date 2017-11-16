from flask import request, render_template, flash, g, \
                render_template_string, session, \
                redirect, url_for, abort, jsonify, send_from_directory,\
                current_app
from flask_jsonpify import jsonpify
import os
import json
from . import main
from ..models import mongo_database


@main.route('/resources_website')
def resources_website():
    """Returns the search page for the resources website"""

    return render_template('wordpress_page.html')


@main.route('/test')
def test():
    # return json.dumps({'msg': "Hello from MolSSI api"})
    return jsonpify({'msg': 'Hello from MolSSI api jsonpify'})


@main.route('/search')
def search_libraries_ui():
    """Search MongoDB for the given query
       Return: HTML formatted data with the results
    """

    results = search_libraries(to_json=False)

    return render_template('libraries.html', libraries=results)


@main.route('/api/search')
def search_libraries(to_json=True):
    """Search MongoDB for the given query
       Return: JSON (array of libraries)
    """

    query = request.args.get('query')
    if query is None:
        query = ''
    languages = json.loads(request.args.get('languages'))
    if languages is None:
        languages = []

    domain = json.loads(request.args.get('domain'))
    print('Search params: {}, {}, {}'.format(query, languages, domain))
    if domain is None:
        domain = []

    results = mongo_database.full_search(query, languages, domain)

    if not to_json:
        return results

    if results:
        json_data = results.to_json()
    else:
        json_data = jsonify('')
    return json_data


@main.route('/contact')
def contact():
    """Return a test JSON file
    """
    json_url = os.path.join(current_app.config['APPLICATION_ROOT'], 'static',
                    'data', 'test.json')
    print(json_url)
    # data = json.load(open(json_url))

    with main.open_resource(json_url) as f:
        data = json.load(f)

    return jsonify(data)

    # For JSONP:
    # return jsonpify({
    #               'name': 'Doaa Altarawy',
    #               'info': 'Research Scientist at MolSSI'
    #               })


@main.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

