from __future__ import print_function
# from molssi_api_flask import app
from molssi_api_flask.core.models.library import Library
from molssi_api_flask.core.mongo_database import *
import pytest


'''
run as a package: python -m tests.mongoEngine_test
Or install and run directly
pip install -e .
python tests/mongoengine_test.py
'''
verbose = False

def setup_module():
    # get_connection('resources_webiste', 'localhost', 27017)
    # creates a test client
    # app = app.test_client()
    # propagate the exceptions to the test client
    # app.testing = True

    get_connection('libraries_test', is_mock=False) # text_search doesn't work in mocks
    clear_libraries()
    load_collection_from_json('./tests/data/test_libs.json')

# def teardown_module():
#     clear_libraries()

def test_create_DB():
    assert Library.objects.count() == 6
    # add_one('Third Library', 'Not this one Unique', ['C++'], 'MM')
    if verbose:
        print_all()

def test_search_text():
    # search_description('Lib')  # --> doesn't work!!
    assert search_text('work', verbose=verbose).count() == 3 # doesn't search stop words, can match plurals of words
    assert search_text('First Third', verbose=verbose).count() == 2
    assert search_text('').count() == 0

def test_search_lanague():
    assert find_language([], verbose=verbose).count() == 0
    assert find_language(['Python'], verbose=verbose).count() == 4
    assert find_language(['C++'], verbose=verbose).count() == 3
    assert find_language(['FORTRAN', 'C++'], verbose=verbose).count() == 5

def test_search_domain():
    assert find_domain([], verbose=verbose).count() == 0
    assert find_domain(['DoesNotExist'], verbose=verbose).count() == 0
    assert find_domain(['QM'], verbose=verbose).count() == 3
    assert find_domain(['MM', 'QM'], verbose=verbose).count() == 6

def test_complex_search():
    assert complex_query([], [], verbose=verbose).count() == 0
    assert complex_query(['Python'], [], verbose=verbose).count() == 0
    assert complex_query([], ['QM'], verbose=verbose).count() == 0
    assert complex_query(['Python'], ['QM'], verbose=verbose).count() == 2

def test_full_search():

    assert full_search(verbose=verbose).count() == 6

    assert full_search('', [], ['DoesNotExist'], verbose=verbose).count() == 0

    assert full_search('', [], ['QM', 'DoesNotExist'], verbose=verbose).count() == 3

    assert full_search('work', ['C++'], ['QM'], verbose=verbose).count() == 1

    assert full_search('first third', ['Python'], ['QM', 'MM'], verbose=verbose).count() == 1

    assert full_search('first third', [], [], verbose=verbose).count() == 2
    #
    assert full_search('', ['Python', 'C++'], [], verbose=verbose).count() == 5
