import requests
from app import create_app, db
from flask import current_app
import pytest
import json
from base64 import b64encode
from app.models.software import Software
from app.models.software import QMFeatures, MMFeatures
import os
from os.path import join, dirname, abspath
import pymongo
from pprint import pprint
from app.models import mongo_database as db_util

headers = {'Content-Type': 'application/json'}


@pytest.mark.usefixtures("app", "client")
class TestDatabase(object):
    """
        Testing database CRUD operations on Software collection

        Import data before running this test:
        mongoimport --db test_db --collection software --type json --jsonArray --file tests/data/software.json
    """

    def test_app_exists(self):
        assert current_app is not None

    def test_database_filled(self, app):
        assert Software.objects.count() == 158

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_add_QM_software(self):
        psi4 = Software.objects(software_name='Psi4').first()
        assert psi4.qm_features
        assert not psi4.mm_features
        # print(psi4.to_json())

    def get_software(self, name):
        return Software.objects(software_name=name).first()

    def test_add_MM_software(self):
        software = self.get_software('LAMMPS')
        # print(software.to_json())
        assert software.mm_features
        assert not software.mm_features.is_empty()

        software.mm_features.qm_mm = True
        software.save()

        id = software.id
        software.software_name = 'LAMMPS' + '2'
        software.id = None
        software.save()

        assert software.id != id

        software.delete()

    def test_search(self):
        assert len(db_util.search_description('LAMMPS')) == 1
        assert len(db_util.search_text('DFT')) == 21
        assert len(db_util.search_text('WXYZ')) == 0
        assert len(db_util.complex_query(['python', 'c'], ['QM'])) == 16

        # test db_util.full_search
