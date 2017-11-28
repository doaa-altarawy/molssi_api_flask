#!venv/bin/python

from __future__ import print_function
from molssi_api_flask.models import mongo_database
import os
import config as config

config = config.config['development']
# config = config.config['production']

#  MongoDB connection
db = mongo_database.get_connection(host=config.MONGODB_SETTINGS['host'])
print('Connecting to DB: ', config.MONGODB_SETTINGS['host'])

#  Clear the DB
mongo_database.clear_libraries()

# Files to be loaded into the DB
# files = ['wiki_QM.json', 'wiki_MM.json']
MM_files = ['MM_curated_data.json']
QM_files = ['QM_curated_data.json']


print('Initial DB size: {}'.format(mongo_database.get_DB_size()))
for filename in MM_files:
    full_path = os.path.join(config.APPLICATION_ROOT, 'data', filename)
    print('Loading file {} in DB....'.format(full_path))
    mongo_database.load_collection_from_json(full_path, lib_type='MM')

    print('After insertion: {}'.format(mongo_database.get_DB_size()))

for filename in QM_files:
    full_path = os.path.join(config.APPLICATION_ROOT, 'data', filename)
    print('Loading file {} in DB....'.format(full_path))
    mongo_database.load_collection_from_json(full_path, lib_type='QM')

    print('After insertion: {}'.format(mongo_database.get_DB_size()))
