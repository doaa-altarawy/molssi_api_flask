from flask import request, render_template, flash, \
                render_template_string, session, \
                redirect, url_for, abort, jsonify, send_from_directory,\
                current_app
import os
import json
from . import main
from ..models import mongo_database
from .forms import SoftwareForm
# from ..admin.admin import SoftwareView
import logging
from flask_login import login_required, current_user
from ..models.search_logs import save_access


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
    """Search MongoDB for software using the given query

        Input filters are passed as get request keys

        Get Request Parameters:
        ---------------
        query_text : str
        domain : MM or QM
        languages : list of str
                   example: ["Python","C","C++","FORTRAN"]
        price : free or non-free (optional, default is free)

        mm_filters : dict of keys (optional)
            e.g., {"file_formats":["CSV","TXT"],"qm_mm":"Yes"}
            - "file_formats" : list ["CSV","TXT"]
            - "qm_mm" : Yes or No
            - "tags": list of supported QM tags,
                e.g., ["PERIODICITY 0D","CONSTRAINTS","MONTE CARLO"]
            - "forcefield_types" : list of str,
                e.g., ["Class I","Polarizable"]}

        qm_filters : dict of QM keys (optional)
        - "basis" : str, e.g., "Gaussian",
        - "element_coverage" : str, e.g., "H..Hg"
        - "tags" : list of supported tags
            e.g., ["DFT","HYBRID"]

        Returns:
        --------
            JSON (array of software)

        Examples:
        ---------
            http://localhost:5000/search?query_text=&domain=QM&languages=["C++","FORTRAN"]
            &price=non-free&qm_filters={"basis":"Gaussian","element_coverage":"H..Hg",
            "tags":["DFT","HYBRID"]}

            http://localhost:5000/search?query_text=&domain=MM&languages=[]&price=free
            &qm_filters={}&mm_filters={"file_formats":["CSV","TXT"],"qm_mm":"Yes",
            "tags":["PERIODICITY 0D","MONTE CARLO"],"forcefield_types":["Class II","Polarizable"]}
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

    if software is None:
        flash("Library not found")
        return render_template('404.html'), 404

    logging.debug("This is software: %s", software.software_name)
    save_access(software)

    return render_template('software_detail.html', lib=software)


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


@main.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)
