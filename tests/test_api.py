from flask import current_app
import pytest
import json
from base64 import b64encode
from app.models.software import Software
from os.path import join, dirname, abspath
import pymongo


headers = {'Content-Type': 'application/json'}


@pytest.mark.usefixtures("app", "client", autouse=True)   # to use fixtures from conftest
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

    def test_home_page(self, client):
        """The API to the root should get all software"""

        response = client.get('/')
        assert response.status_code == 200
        assert 'MolSSI' in response.get_data(as_text=True)

    def test_empty_search(self, client):
        """Default (empty) search results in all none pending software
         in the DB
         """

        # http://localhost:5000/api/search?query_text=&domain=&languages=[]
        params = dict(query_text='', domain='', languages='[]')
        response = client.get(self.api_url, query_string=params) #, headers=headers)
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))
        # 60 none pending software out of 158 in the test DB
        assert len(json_data) == 63

    def test_empty_formatted_search(self, client):
        """Get the default formatted for the default search
         """

        params = dict(query_text='', domain='', languages='[]')
        response = client.get(self.template_url, query_string=params)
        assert response.status_code == 200

        formatted_data = response.get_data(as_text=True)
        assert 'ABINIT' in formatted_data
        assert 'ACES' in formatted_data
        assert '</div>' in formatted_data

    def test_get_software_details(self, client):
        url = 'software_detail/5aa1926f750213c7dc3f210b'
        response = client.get(url)
        assert response.status_code == 200

        assert 'GAMESS (UK)' in response.get_data(as_text=True)
        assert 'Compilers' in response.get_data(as_text=True)
        assert 'Documentation' in response.get_data(as_text=True)

    def test_get_software_details_notfound(self, client):
        url = 'software_detail/wrong_id'
        response = client.get(url)
        assert response.status_code == 404

    @pytest.mark.parametrize("query, result_size", [
        (dict(query_text='', domain='', languages='[]'), 63),
        (dict(query_text='', domain='', languages='[]', price='free',
              qm_filters={}, mm_filters={}), 44),
        (dict(query_text='', domain='QM', languages='[]'), 41),
        (dict(query_text='', domain='MM', languages='[]'), 16),
        (dict(query_text='', domain='', languages='[]', price='free'), 44),
        (dict(query_text='', domain='', languages='[]', price='non-free'), 28),
    ])
    def test_search(self, client, query, result_size):
        """Regression test for several filters
        """
        response = client.get(self.api_url, query_string=query)
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))
        assert len(json_data) == result_size

    @pytest.mark.parametrize("query, result_size", [
        (dict(query_text='', domain='MM', languages='[]'), 16),
        (dict(query_text='OpenMM', domain='MM', languages='[]'), 3),
        (dict(query_text='', domain='MM', languages='[]', price='free'), 12),
        (dict(query_text='', domain='MM', languages='[]', price='non-free'), 8),
        (dict(query_text='', domain='MM', languages='["Python","C"]'), 6),
        (dict(query_text='', domain='MM', languages='[]',
              mm_filters={
                          "file_formats": ["CSV", "TXT"],
                          "qm_mm": "Yes",
                          "tags": ["PERIODICITY 0D", "CONSTRAINTS", "MONTE CARLO"],
                          "forcefield_types": ["Class I", "Polarizable"]
                          }), 1)  # OpenMM
    ])
    def test_search_MM(self, client, query, result_size):
        """Regression test for several filters
        """
        response = client.get(self.api_url, query_string=query)
        assert response.status_code == 200

        json_data = json.loads(response.get_data(as_text=True))
        assert len(json_data) == result_size


    # @pytest.mark.parametrize()
    # def test_possible_filters(self, client, ):
    #     """Search using many possible filters
    #     """
    #     params = dict(query_text='', domain='', languages='[]')
    #     response = client.get(self.api_url, query_string=params)
    #     assert response.status_code == 200
    #
    #     json_data = json.loads(response.get_data(as_text=True))
    #     # assert len(json_data) == 0


{
    'qm_filters': u'{}',
    'domain': u'MM',
    'mm_filters':
        u'{"file_formats":["CSV","TXT"],"qm_mm":"Yes"}',
    'price': u'',
    'languages': u'[]',
    'query_text': u''}

{
    'query_text': '',
    'domain': 'MM',
    'mm_filters':
        "{'file_formats': ['CSV', 'TXT'], 'qm_mm': 'Yes'}"}