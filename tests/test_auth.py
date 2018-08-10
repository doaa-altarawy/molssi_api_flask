from app import create_app, db
from flask import current_app
import pytest
import json
from base64 import b64encode
from app.models.users import User


class TestAuth(object):
    """
        Testing User authentication, login, logout
    """

    @classmethod
    def setup_class(cls):
        cls.auth_url = '/auth'
        app = create_app('testing')
        cls.app_context = app.app_context()
        cls.app_context.push()
        cls.client = app.test_client()
        # cls.client = cls.app.test_client(use_cookies=True)
        cls.fill_db()

    @classmethod
    def teardown_class(cls):
        # User.objects().delete()
        cls.app_context.pop()

    @classmethod
    def fill_db(cls):
        """Fill the test DB with the admin user
            The admin is user whose email is defined in Flask
            config in APP_ADMIN
        """
        User.objects.delete()
        user = User(email='daltarawy@vt.edu',
                    full_name='Doaa Test')
        user.password = 'fakePass'
        user.confirmed = True
        user.save()

    def test_app_exists(self):
        assert current_app is not None

    def test_database_filled(self):
        assert User.objects(email='daltarawy@vt.edu').count() == 1

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_register(self):
        # get registration form
        response = self.client.get((self.auth_url+'/register'))
        assert response.status_code == 200

        data = dict(email='dina@gmail.com', password='somePass',
                    password2='somePass', full_name='Dina')
        response = self.client.post(self.auth_url+'/register', data=data)
        # on success, redirect to home
        assert response.status_code == 302
        assert '/auth/login' in response.get_data(as_text=True)
        # print(response.get_data(as_text=True))

    def test_register_exiting_email(self):
        data = dict(email='daltarawy@vt.edu', password='somePass',
                    password2='somePass', full_name='Doaa')
        response = self.client.post(self.auth_url+'/register', data=data)
        assert response.status_code == 200
        assert 'Email already registered' in response.get_data(as_text=True)

    def test_sign_in(self):
        data = dict(email='daltarawy@vt.edu', password='fakePass')
        response = self.client.post(self.auth_url+'/login', data=data,
                                    follow_redirects=True)
        # on success, redirect to home
        assert response.status_code == 200
        assert '/admin/' in response.get_data(as_text=True)
        assert 'Change Email' in response.get_data(as_text=True)
        assert 'Change Password' in response.get_data(as_text=True)

    def test_wrong_sign_in(self):
        data = dict(email='daltarawy@vt.edu', password='wrongPass')
        response = self.client.post(self.auth_url+'/login', data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'Invalid email or password' in response.get_data(as_text=True)

    def test_sign_out(self):
        # make sure you are logged in first
        data = dict(email='daltarawy@vt.edu', password='fakePass')
        response = self.client.post(self.auth_url+'/login', data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'Change Email' in response.get_data(as_text=True)
        # logout
        response = self.client.get(self.auth_url+'/logout',
                                   follow_redirects=True)
        assert 'You have been logged out' in response.get_data(as_text=True)
