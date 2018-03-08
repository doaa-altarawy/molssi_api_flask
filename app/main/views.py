from flask import request, render_template, flash, g, \
                render_template_string, session, \
                redirect, url_for, abort, jsonify, send_from_directory,\
                current_app
from flask_jsonpify import jsonpify
import os
import json
from . import main
from ..models import mongo_database
from .forms import SoftwareForm
from ..admin.admin import SoftwareView
import logging
from flask_login import login_required, current_user


@main.route('/')
@main.route('/resources_website')
@main.route('/cms_software_db')
@main.route('/software-search')  # preferred name
def index():
    """Returns the search page for the resources website"""
    lib = mongo_database.get_lib_features()

    return render_template('wordpress_page.html', lib=lib)


@main.route('/search')
def search_libraries_ui():
    """Search MongoDB for the given query
       Return: HTML formatted data with the results
    """

    results = search_libraries(to_json=False)

    return render_template('software_list.html', libraries=results)


@main.route('/api/search')
def search_libraries(to_json=True):
    """Search MongoDB for the given query
       Return: JSON (array of libraries)
    """

    # query_text = request.args.get('query_text', '', type=str)

    # languages = json.loads(request.args.get('languages', '[]'))
    # if languages is None:
    #     languages = []
    #
    # domain = request.args.pop('domain', '')
    # price = request.args.pop('price', '', type=str)

    logging.info('Flask received Search params: {}'.format(request.args.to_dict()))

    exec_empty_sw = current_app.config['EXCLUDE_EMPTY_SW']
    results = mongo_database.full_search(exec_empty_sw, **request.args.to_dict())

    if not to_json:
        return results

    if results:
        json_data = results.to_json()
    else:
        json_data = jsonify('')
    return json_data


@main.route('/software_detail/<sw_id>', methods=['GET'])
# @login_required
# @admin_required
# @permission_required(Permission.MODERATE)
def software_detail(sw_id):
    logging.info('Find software with ID: %s', sw_id)
    software = mongo_database.get_software(sw_id)
    logging.debug("This is software: %s", software.software_name)
    if software is None:
        flash("Library not found")

    return render_template('software_detail.html', lib=software)


@main.route('/software/<sw_id>', methods=['GET', 'POST'])
def software_form(sw_id):
    software = mongo_database.get_software(sw_id)
    logging.debug("This is software: ", software.software_name)

    form = SoftwareForm()

    return render_template('software_form.html', form=form)


@main.route('/contact')
def contact():
    """Return a test JSON file
    """
    json_url = os.path.join(current_app.config['base_dir'], 'static',
                    'data', 'test.json')
    logging.debug(json_url)
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


@main.route('/success')
def add_software_success():
    """Success page after adding a new software"""

    return render_template('software_added_success.html')
