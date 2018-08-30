from flask import request
import pytest
import json
from base64 import b64encode
from app.models.software import Software
from app.models.users import User


# to use fixtures from conftest
@pytest.mark.usefixtures("app", "client", "form_empty", "form_full", autouse=True)
class TestSubmitSoftware(object):
    """
        Testing submitting software by the users

        Import data before running this test:
        mongoimport --db test_db --collection software --type json --jsonArray
                --file tests/data/software.json
    """

    @classmethod
    def setup_class(cls):
        cls.admin_url = '/admin'
        cls.auth_url = '/auth'

    @pytest.fixture(scope='class', autouse=True)
    def fill_db(self, app):
        """Fill the test DB """
        pass

    def test_database_filled(self):
        assert Software.objects.count() == 158

    def logout(self, client):
        return client.get(self.auth_url+'/logout', follow_redirects=True)

    def test_submit_software_home(self, client):
        """View submit software page (no login required)"""

        # Doesn't require login
        assert self.logout(client)

        response = client.get(self.admin_url + '/submit_software/',
                              follow_redirects=True)

        assert 'Submit Software for review' in response.get_data(as_text=True)

    def test_submit_software_empty(self, client, form_empty):
        """Test submitting a software with missing required fields"""

        # Doesn't require login
        assert self.logout(client)

        response = client.post(self.admin_url + '/submit_software/',
                               data=form_empty, follow_redirects=True)

        assert 'Submit Software for review' in response.get_data(as_text=True)
        assert 'Some fields are missing' in response.get_data(as_text=True)
        assert 'This field is required' in response.get_data(as_text=True)

    def test_submit_software_full(self, client, form_full):
        """Submit a full software successfully"""

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

    def test_edit_software(self, client, form_full):
        """Test edit software after submission"""

        # Doesn't require login
        assert self.logout(client)

        form_full['software_name'] = 'test_software_submit'
        response = client.post(self.admin_url + '/submit_software/',
                               data=form_full, follow_redirects=True)

        assert 'Thank you. The software was submitted successfully' \
               in response.get_data(as_text=True)
        assert "To preview your submitted software" in response.get_data(as_text=True)

        # get edit URL from response
        edit_url = response.get_data(as_text=True).split(
                                'To edit your submitted software: <a href="')[-1]
        edit_url = edit_url.split('" target="_blank">')[0]
        # print(edit_url)

        # review the submitted page
        response = client.get(edit_url, follow_redirects=True)

        assert 'test_software_submit' in response.get_data(as_text=True)
        assert 'Submit Software for review' in response.get_data(as_text=True)

        # edit software and submit
        form_full['software_name'] = 'test_software_edited'
        response = client.post(edit_url, follow_redirects=True, data=form_full)

        assert 'Thank you. The software was submitted successfully' \
               in response.get_data(as_text=True)

        # clean up
        Software.objects(software_name='test_software_edited').delete()

    def test_edit_software_notfound(self, client, form_full):
        """Test edit software after submission (not found)"""

        # review the submitted page (with wrong URL)
        response = client.get(self.admin_url + '/submit_software/edit/wrong_token',
                              follow_redirects=True)

        assert 'Software does not exist or the URL has expired.' \
               in response.get_data(as_text=True)
