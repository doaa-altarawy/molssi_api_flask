from __future__ import print_function
from mongoengine import connect
from molssi_api_flask.core.models.library import Library
from mongoengine.queryset.visitor import Q
import json


'''
Search operators:
-----------------

a) Numbers:

Example: Libary.objects(name__ne='Python')
    ne: not equal to
    lt: less than
    lte: less than or equal to
    gt: greater than
    gte: greater than or equal to
    not: negate a standard check, may be used before other operators (e.g. Q(age__not__mod=5))
    in: value is in list (a list of values should be provided)
    nin: value is not in list (a list of values should be provided)
    mod: value % x == y, where x and y are two provided values
    all: every item in list of values provided is in array
    size: the size of the array is
    exists: value for field exists


b) Strings:

    exact: string field exactly matches value
    iexact: string field exactly matches value (case insensitive)
    contains: string field contains value
    icontains: string field contains value (case insensitive)
    startswith: string field starts with value
    istartswith: string field starts with value (case insensitive)
    endswith: string field ends with value
    iendswith: string field ends with value (case insensitive)
    match: performs an $elemMatch so you can match an entire document within an array


Query with:
Library.object(..) --> no exception, can return 0+, returns a queryset
Library.get(..) --> return exactly one, raises exception otherwise
                    (DoesNotExist, MultipleObjectsReturned)

queryset Functions:
.count()
.order_by('field_name')
.sum('field_name')


Create Objects:
---------------
Library.objects.insert(my_lib_object)
Library.objects.insert(  Library(**my_lib_json)  )

Multiple:
Library.objects.insert([mylib1, mylib2, mylib3])

my_library.save()
my_library.update(params)

Library.objects(..).delete()


json_list = Library.objects(..).to_json()
from_json??
'''


def get_connection(name='', host='localhost', port=27017, is_mock=False):
    """ Create MongoDB using mongoengine
        use is_mock to Create a mock empty DB for testing
    """
    if is_mock:
        # mock connection for testing
        return connect('mongoenginetest', host='mongomock://localhost')
    if name:
        return connect(name, host=host, port=port)

    return connect(host=host)


def clear_libraries():
    """Clear Libraries Collections"""
    Library.objects().delete()


def load_collection_from_json(filename):
    """Load DB from a Json file with list of JSON objects of libraries"""

    with open(filename) as f:
        json_list = json.load(f)

    library_list = []
    for json_data in json_list:
        library_list.append(Library(**json_data))

    Library.objects.insert(library_list)


# ---------------------------   Query functions  ------------------------ #

def find_language(lang, verbose=False):
    results = Library.objects(languages__in=lang)
    if verbose:
        print('Num of results for {} is {}'.format(lang, results.count()))
        print_results(results)
    return results


def find_domain(domain, verbose=False):
    results = Library.objects(domain__in=domain)
    if verbose:
        print('Num of results for {} is {}'.format(domain, results.count()))
        print_results(results)

    return results


def search_description(keyword, verbose=False):
    """Search descrption """
    # TODO: fixme

    results = Library.objects(description__contains(keyword))
    if verbose:
        print('Num of results for {} is {}'.format(keyword, results.count()))
        print_results(results)

    return results


def search_text(query, verbose=False):
    """search indexed text fields (defined with $ in meta)"""
    results = Library.objects.search_text(query)

    if results:
        results = results.order_by('$text_score')

    if verbose:
        print_results(results)

    return results


def complex_query(languages=[], domains=[], verbose=False):
    results = Library.objects(Q(languages__in=languages) & Q(domain__in=domains))
    if verbose:
        print_results(results)

    return results


def full_search(query='', languages=[], domains=[], verbose=False):
    """Search the libraries collection using joint search of multiple fields
        any empty field will not be searched.
        if all fields are empty, then all documents are returned
        Note: fields must not be None
    """

    results = None

    if len(languages) != 0 and len(domains) != 0:
        results = Library.objects(Q(languages__in=languages) & Q(domain__in=domains))
    elif len(languages) != 0:
        results = Library.objects(languages__in=languages)
    elif len(domains) != 0:
        results = Library.objects(domain__in=domains)

    if len(query) != 0:
        if results:
            results = results.search_text(query)
        else:
            results = Library.objects.search_text(query)
        if results:
            results = results.order_by('$text_score')
    else:
        if results:
            results = results.order_by('name')

    if len(languages) == 0 and len(domains) == 0 and len(query) == 0:  # return all libraries
        results = Library.objects.order_by('name')

    if verbose:
        print_results(results)

    return results


def get_json(verbose=False):
    """Get json data of the DB"""

    json_data = Library.objects().to_json()
    if verbose:
        print(json_data)

    return json_data

# ----------------------- Printing and Utils ------------------------- #


def add_one(name, description='', languages='', domain='', verbose=False):
    my_lib = Library(
        name=name,
        description=description,
        languages=languages,
        domain=domain
    )

    my_lib.save()
    if verbose:
        print('Added: ', my_lib)

    return my_lib


def print_results(results):
    """For testing"""
    if results:
        for res in results:
            print(res)
    print('........')


def print_all():
    """Print all Documents in the Libraries collection"""

    all_libs = Library.objects
    print('Currently in DB: ', all_libs.count())
    print_results(all_libs)
