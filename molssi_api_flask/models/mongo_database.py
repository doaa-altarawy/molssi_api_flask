from __future__ import print_function
from mongoengine import connect
from .library import Library, QMFeatures, MMFeatures, create_library
from mongoengine.queryset.visitor import Q
import json
import re


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
    # db.drop_database('resources_website')


def load_collection_from_json(filename, lib_type=None):
    """Load DB from a Json file with list of JSON objects of libraries"""

    with open(filename) as f:
        json_list = json.load(f)

    for json_record in json_list:
        library = create_library(lib_type, **json_record)
        library.save(validate=False)

    # [Library(**json_record).save(validate=False) for json_record in json_list]

    # Library.objects.insert(library_list) # doesn't call override save


# ---------------------------   Query functions  ------------------------ #

def find_language(lang, verbose=False):
    results = Library.objects(languages_lower__in=lang.lower())
    if verbose:
        print('Num of results for {} is {}'.format(lang.lower(), results.count()))
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
    languages_lower = [lang.lower() for lang in languages]
    results = Library.objects(Q(languages_lower__in=languages_lower) & Q(domain__in=domains))
    if verbose:
        print_results(results)

    return results


def full_search(exec_empty_lib=False, verbose=False, **kwargs):
    """Search the libraries collection using joint search of multiple fields
        any empty field will not be searched.
        if all fields are empty, then all documents are returned
        Note: fields must not be None
    """

    results = None
    query, qm_filters, mm_filters = {}, {}, {}
    arg_query = ''

    query_text = kwargs.pop('query_text', '')

    if kwargs.get('qm_filters'):
        qm_filters = json.loads(kwargs.pop('qm_filters', ''))
    if kwargs.get('mm_filters'):
        mm_filters = json.loads(kwargs.pop('mm_filters', ''))

    # ----------- MM filters ------------
    if 'qm_mm' in mm_filters:
        if mm_filters['qm_mm'] == 'Yes':
            query['mm_features__qm_mm__exists'] = True
        else:
            query['mm_features__qm_mm__exists'] = False

    if 'ensembles' in mm_filters:
        query['mm_features__ensembles'] = get_compiled_regex(mm_filters['ensembles'])

    # ----------- QM filters ------------
    if 'basis' in qm_filters:
        query['qm_features__basis__icontains'] = qm_filters['basis']
    if 'coverage' in qm_filters:
        query['qm_features__coverage__icontains'] = qm_filters['coverage']

    # ------------ other filters -----------
    languages = json.loads(kwargs.pop('languages', ''))
    if len(languages) != 0:
        query['languages_lower__in'] = [lang.lower() for lang in languages]

    price = kwargs.pop('price', '')
    if price == 'free':
        query['price__icontains'] = price
    elif price == 'non-free':
        query['price__nin'] = ['free']
        query['price__exists'] = True
    elif price == 'unknown':
        query['price__exists'] = False

    # add the rest of the keywords
    for key, val in kwargs.items():
        if val:
            query[key] = val

    if exec_empty_lib:
        # non_empty = {'$or': [{'description__ne': ''}, {'long_description__ne': ''}]}
        arg_query = (Q(description__ne='') | Q(long_description__ne=''))

    print('MongoDB query:', query)
    results = Library.objects(arg_query, **query)

    print('Results length: ', len(results))

    # if len(languages_lower) != 0 and len(domain) != 0:
    #     results = Library.objects(Q(languages_lower__in=languages_lower) & Q(domain__in=domain))
    # elif len(languages_lower) != 0:
    #     results = Library.objects(languages_lower__in=languages_lower)
    # elif len(domain) != 0:
    #     results = Library.objects(domain__in=domain)
    # print(results)

    if len(query_text) != 0:
        if results:
            results = results.search_text(query_text)
        else:
            results = Library.objects.search_text(query_text)
        if results:
            results = results.order_by('$text_score')
    else:
        if results:
            results = results.order_by('name')

    # if len(languages_lower) == 0 and len(domain) == 0 and len(query_text) == 0:  # return all libraries
    #     results = Library.objects.order_by('name')

    if verbose:
        print_results(results)

    return results


def get_compiled_regex(search_string):
    """Returns a complied regular expression string
    from a query string of space-separated terms"""

    w_list = ['.*' + term + '.*' for term in search_string.split()]
    regex = re.compile('|'.join(w_list), re.IGNORECASE)

    return regex


def get_json(verbose=False):
    """Get json data of the DB"""

    json_data = Library.objects().to_json()
    if verbose:
        print(json_data)

    return json_data


def get_library(lib_id):
    libs = Library.objects(id=lib_id)
    if libs:    # return first result
        return libs[0]
    else:
        return None


def get_lib_features():
    """Get different values for Library properties values
        Used for search queries."""
    lib = {
        'mm_props': {},
        'qm_props': {}
    }
    lib['mm_props']['TAG_NAMES'] = MMFeatures.TAG_NAMES
    lib['qm_props']['TAG_NAMES'] = QMFeatures.TAG_NAMES

    return lib

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


def get_DB_size():
    return Library.objects.count()
