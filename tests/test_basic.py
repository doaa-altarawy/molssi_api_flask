import requests
from app import create_app, db
from flask import current_app
import pytest


url = 'http://localhost:5000/api/search'
# url = 'http://localhost:5000/search'  # UI interface
headers = {'Content-Type': 'application/json'}


def setup_module():
    """ setup any state specific to the execution of the given module."""
    pass

def teardown_module():
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    pass


class TestBasicApp(object):

    def setup_class(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()

    def teardown_class(self):
        # db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        assert current_app is not None

    def test_app_is_testing(self):
        assert current_app.config['TESTING']

    def test_empty_search(self):

        params = dict(query='', domain='[]', languages='["Python"]')
        response = requests.get(url, params=params, headers=headers)

        print(response.status_code)
        assert response.status_code == 200
        print(response.json())
