from app import create_app
from flask import current_app


class TestBasicApp(object):
    """
        Test creating a Flask app in Testing mode
    """

    @classmethod
    def setup_class(cls):
        app = create_app('testing')
        cls.app_context = app.app_context()
        cls.app_context.push()

    def teardown_class(cls):
        cls.app_context.pop()

    def test_app_exists(self):
        assert current_app is not None

    def test_app_is_testing(self):
        assert current_app.config['TESTING']
