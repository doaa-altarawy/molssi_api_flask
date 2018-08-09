from flask import render_template, request, jsonify
from . import main


# @main.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    else:
        return render_template('404.html'), 404
