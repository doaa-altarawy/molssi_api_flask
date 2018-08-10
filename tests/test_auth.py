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

    def login_admin(self):
        self.client.get(self.auth_url+'/logout', follow_redirects=True)
        data = dict(email='daltarawy@vt.edu', password='fakePass')
        response = self.client.post(self.auth_url+'/login', data=data,
                                    follow_redirects=True)
        success = 'Change Email' in response.get_data(as_text=True)
        return success

    def logout(self):
        return self.client.get(self.auth_url+'/logout', follow_redirects=True)

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

        # test unconfirmed
        self.logout()
        data = dict(email='dina@gmail.com', password='somePass')
        response = self.client.post(self.auth_url+'/login', data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'You have not confirmed your account yet' \
               in response.get_data(as_text=True)

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

    def test_change_password(self):
        # log in as admin
        assert self.login_admin()
        response = self.client.get(self.auth_url+'/change-password')
        assert response.status_code == 200
        assert 'Old password' in response.get_data(as_text=True)

        # new password does not match
        data = dict(old_password='wrong', password='123', password2='456')
        response = self.client.post(self.auth_url+'/change-password', data=data)
        assert response.status_code == 200
        assert 'Passwords must match' in response.get_data(as_text=True)

        # wrong old password
        data = dict(old_password='wrong', password='1234567', password2='1234567')
        response = self.client.post(self.auth_url+'/change-password', data=data)
        assert response.status_code == 200
        assert 'Invalid password' in response.get_data(as_text=True)

        # correct entry
        data = dict(old_password='fakePass', password='1234567', password2='1234567')
        response = self.client.post(self.auth_url+'/change-password', data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'Your password has been updated' in response.get_data(as_text=True)

        # change password back to original, redirect of success
        data = dict(old_password='1234567', password='fakePass', password2='fakePass')
        response = self.client.post(self.auth_url+'/change-password', data=data)
        assert response.status_code == 302

    def test_change_email(self):
        # log in as admin
        assert self.login_admin()
        response = self.client.get(self.auth_url+'/change_email')
        assert response.status_code == 200
        assert 'Change Your Email Address' in response.get_data(as_text=True)

        # Email already exist
        data = dict(email='daltarawy@vt.edu', password='fakePass')
        response = self.client.post(self.auth_url+'/change_email', data=data)
        assert response.status_code == 200
        assert 'Email already registered' in response.get_data(as_text=True)

        # Wrong password
        data = dict(email='daltarawy2@vt.edu', password='wrong')
        response = self.client.post(self.auth_url+'/change_email', data=data)
        assert response.status_code == 200
        assert 'Invalid password' in response.get_data(as_text=True)

        # correct entry
        data = dict(email='daltarawy2@vt.edu', password='fakePass')
        response = self.client.post(self.auth_url+'/change_email', data=data,
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'confirm your new email address' in response.get_data(as_text=True)

    def test_reset_password(self):
        # if already logged in, redirect to home
        self.login_admin()
        response = self.client.get(self.auth_url+'/reset', follow_redirects=True)
        assert 'Change Email' in response.get_data(as_text=True)

        # Logout and reset password
        self.logout()
        response = self.client.get(self.auth_url+'/reset', follow_redirects=True)
        assert response.status_code == 200
        assert 'Reset Your Password' in response.get_data(as_text=True)

        response = self.client.post(self.auth_url+'/reset',
                                    data=dict(email='someEmail@vt.edu'),
                                    follow_redirects=True)
        assert response.status_code == 200
        assert 'An email with instructions to reset your password' \
               in response.get_data(as_text=True)
