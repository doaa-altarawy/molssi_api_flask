import pytest
import json


@pytest.mark.usefixtures("app", "client")
class TestFlaskClient(object):
    """
        Test creating a Flask app and a client
        connect to the client without access to DB
    """

    @pytest.mark.parametrize('url', ['/', '/software-search'])
    def test_home_page(self, url, client):
        """Test accessing the website from alternative paths of homepage"""

        response = client.get(url)
        assert response.status_code == 200
        assert 'MolSSI' in response.get_data(as_text=True)

    def test_404_json(self, client):
        headers = {'Accept': 'application/json'}
        response = client.get('/wrong/url', headers=headers)
        assert response.status_code == 404
        json_response = json.loads(response.get_data(as_text=True))
        assert json_response['error'] == 'not found'

    def test_404(self, client):
        response = client.get('/wrong/url')
        assert response.status_code == 404
        assert 'Page Not Found' in response.get_data(as_text=True)
