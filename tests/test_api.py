import requests
from app import create_app, db
from flask import current_app
import pytest
import json
from base64 import b64encode
from app.models.software import Software, create_software
import os
from os.path import join, dirname, abspath
import pymongo

headers = {'Content-Type': 'application/json'}


class TestAPIs(object):
    """
        Testing the APIs by connecting to the flask app from a client.
        A testing DB is used, filled with test data, and cleared afterward

        Import data before running this test:
        mongoimport --db test_db --collection software --type json --jsonArray
                --file tests/data/software.json
    """

    @classmethod
    def setup_class(cls):
        cls.api_url = '/api/search'
        cls.template_url = '/search'
        app = create_app('testing')
        cls.app_context = app.app_context()
        cls.app_context.push()
        cls.client = app.test_client()
        # cls.client = cls.app.test_client(use_cookies=True)
        cls.fill_db()

    @classmethod
    def teardown_class(cls):
        # Software.objects().delete()
        cls.app_context.pop()

    @classmethod
    def fill_db(cls):
        """Fill the test DB with some tests data from json"""

        data_path = join(dirname(abspath(__file__)), 'data')
        data_path = join(data_path, 'software.json')
        pymongo.MongoClient('mongoimport --db test_db --collection software '
                            + '--type json --jsonArray --file ' + data_path)
        # with open(data_path) as f:
        #     json_list = json.load(f)
        #
        # Software.objects().delete()     # make sure it's empty
        # for software in json_list:
        #     print(software)
        #     # del software['_id']
        #     # sw = create_software(**software)
        #     # sw = Software().from_json(json.dumps(software))
        #     # sw.save(validate=False)

    def test_app_exists(self):
        assert current_app is not None

    def test_database_filled(self):
        assert Software.objects.count() == 158

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_home_page(self):
        """The API to the root should get all software"""

        response = self.client.get('/')
        assert response.status_code == 200
        assert 'MolSSI' in response.get_data(as_text=True)

    def test_empty_search(self):
        """Default (empty) search results in all none pending software
         in the DB
         """

        # http://localhost:5000/api/search?query_text=&domain=&languages=[]
        params = dict(query_text='', domain='', languages='[]')
        response = self.client.get(self.api_url, query_string=params) #, headers=headers)
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))
        # 60 none pending software out of 158 in the test DB
        assert len(json_data) == 60

    def test_empty_formatted_search(self):
        """Get the default formatted for the default search
         """

        params = dict(query_text='', domain='', languages='[]')
        response = self.client.get(self.template_url, query_string=params)
        assert response.status_code == 200

        formatted_data = response.get_data(as_text=True)
        assert 'ABINIT' in formatted_data
        assert 'ACES' in formatted_data
        assert '</div>' in formatted_data

    def test_get_software_details(self):
        url = 'software_detail/5aa1926f750213c7dc3f210b'
        response = self.client.get(url)
        assert response.status_code == 200

        assert 'GAMESS (UK)' in response.get_data(as_text=True)
        assert 'Compilers' in response.get_data(as_text=True)
        assert 'Documentation' in response.get_data(as_text=True)

    def test_get_software_details_notfound(self):
        url = 'software_detail/wrong_id'
        response = self.client.get(url)
        assert response.status_code == 404




