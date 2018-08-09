from app import create_app
import pytest
import json


class TestFlaskClient(object):
    """
        Test creating a Flask app and a client
        connect to the client without access to DB
    """
    app_context = None
    client = None

    @classmethod
    def setup_class(cls):
        app = create_app('testing')
        cls.app_context = app.app_context()
        cls.app_context.push()
        cls.client = app.test_client(use_cookies=True)

    @classmethod
    def teardown_class(cls):
        cls.app_context.pop()

    @pytest.mark.parametrize('url', ['/', '/software-search'])
    def test_home_page(self, url):
        """Test accessing the website from alternative paths of homepage"""

        response = self.client.get(url)
        assert response.status_code == 200
        assert 'MolSSI' in response.get_data(as_text=True)

    def test_404(self):
        headers = {'Accept': 'application/json'}
        response = self.client.get('/wrong/url', headers=headers)
        assert response.status_code == 404
        json_response = json.loads(response.get_data(as_text=True))
        assert json_response['error'] == 'not found'
