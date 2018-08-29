from flask import current_app
import pytest
import json
from base64 import b64encode
from app.models.software import Software
from app.models.users import User


# to use fixtures from conftest
@pytest.mark.usefixtures("app", "client", "form_empty", "form_full", autouse=True)
class TestAdmin(object):
    """
        Testing the Admin interface for data curation

        Import data before running this test:
        mongoimport --db test_db --collection software --type json --jsonArray
                --file tests/data/software.json
    """

    @classmethod
    def setup_class(cls):
        cls.admin_url = '/admin'
        cls.auth_url = '/auth'

    # prerequisite for all other tests
    @pytest.fixture(scope='class', autouse=True)
    def fill_db(self, app):
        """Fill the test DB with admin user"""

        User.objects.delete()
        user = User(email='daltarawy@vt.edu',
                    full_name='Doaa Test')
        user.password = 'fakePass'
        user.confirmed = True
        user.save()

    def test_database_filled(self):
        assert Software.objects.count() == 158

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_admin_home_page(self, client):
        """The Admin home needs login"""

        response = client.get(self.admin_url, follow_redirects=True)

        assert 'DB Admin' in response.get_data(as_text=True)
        assert 'Log In' in response.get_data(as_text=True)

    def login(self, client):
        data = dict(email='daltarawy@vt.edu', password='fakePass')
        response = client.post(self.auth_url+'/login', data=data,
                               follow_redirects=True)
        success = 'Change Email' in response.get_data(as_text=True)
        return success

    def logout(self, client):
        return client.get(self.auth_url+'/logout', follow_redirects=True)

    def test_admin_home_page_login(self, client):
        """The Admin home with login"""

        assert self.login(client)
        response = client.get(self.admin_url, follow_redirects=True)

        assert 'DB Admin' in response.get_data(as_text=True)
        assert 'Log Out' in response.get_data(as_text=True)

    def test_admin_software(self, client):
        """Test showing software list"""

        assert self.login(client)
        response = client.get(self.admin_url + '/software', follow_redirects=True)

        assert 'List (158)' in response.get_data(as_text=True)
        assert 'Log Out' in response.get_data(as_text=True)

    def test_admin_users(self, client):
        """Test showing user list"""

        assert self.login(client)
        response = client.get(self.admin_url + '/user', follow_redirects=True)

        assert 'List (1)' in response.get_data(as_text=True)
        assert 'Administrator' in response.get_data(as_text=True)

    def test_admin_search_logs(self, client):
        """Test showing search logs"""

        assert self.login(client)
        response = client.get(self.admin_url + '/softwareaccess/', follow_redirects=True)

        assert 'Access Date' in response.get_data(as_text=True)
        assert 'Ip Address' in response.get_data(as_text=True)

    def test_admin_view_submit_software(self, client):
        """View submit software page (no login required)"""

        # Doesn't require login
        assert self.logout(client)

        response = client.get(self.admin_url + '/submit_software/', follow_redirects=True)
        assert 'Submit Software for review' in response.get_data(as_text=True)

    def test_admin_new_software_empty(self, client, form_empty):
        """Add new software from Admin (needs login)"""

        assert self.login(client)

        response = client.post(self.admin_url + '/software/new/', data=form_empty,
                               follow_redirects=True)

        assert 'Please fill this form' in response.get_data(as_text=True)
        assert 'This field is required' in response.get_data(as_text=True)

    def test_admin_new_software_full(self, client, form_full):
        """Add new software from Admin (needs login)"""

        assert self.login(client)

        form_full['software_name'] = 'test_software_new'
        response = client.post(self.admin_url + '/software/new/', data=form_full,
                               follow_redirects=True)

        assert 'Record was successfully created' \
               in response.get_data(as_text=True)

        Software.objects(software_name='test_software_new').delete()

    def test_admin_submit_software(self, client, form_empty):
        """The Admin home with login"""

        # Doesn't require login
        assert self.logout(client)

        response = client.post(self.admin_url + '/submit_software/',
                               data=form_empty, follow_redirects=True)

        assert 'Submit Software for review' in response.get_data(as_text=True)
        assert 'Some fields are missing' in response.get_data(as_text=True)
        assert 'This field is required' in response.get_data(as_text=True)

    def test_admin_submit_software_full(self, client, form_full):
        """The Admin home with login"""

        # Doesn't require login
        assert self.logout(client)

        form_full['software_name'] = 'test_software_submit'
        response = client.post(self.admin_url + '/submit_software/',
                               data=form_full, follow_redirects=True)

        assert 'Thank you. The software was submitted successfully' \
               in response.get_data(as_text=True)
        assert "To preview your submitted software" in response.get_data(as_text=True)
        assert 'To edit your submitted software: ' in response.get_data(as_text=True)

        Software.objects(software_name='test_software_submit').delete()
