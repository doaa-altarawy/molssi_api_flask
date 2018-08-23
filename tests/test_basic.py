# from app import create_app
from flask import current_app
import pytest


@pytest.mark.usefixtures("app", "client")
class TestBasicApp(object):
    """
        Test creating a Flask app in Testing mode
    """

    def test_app_exists(self):
        assert current_app is not None

    def test_app_is_testing(self):
        assert current_app.config['TESTING']
