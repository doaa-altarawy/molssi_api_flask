from __future__ import print_function
from molssi_api_flask.core import mongo_database as db
import os
import config as config

#  MongoDB connection
db.get_connection(config.DB_NAME, config.DB_HOST, config.DB_PORT)

#  Clear the DB
db.clear_libraries()

# Files to be loaded into the DB
files = ['wiki_QM.json', 'wiki_MM.json']

print('Initial DB size: {}'.format(db.full_search().count()))
for filename in files:
    full_path = os.path.join(config.APPLICATION_ROOT, 'data', filename)
    print('Loading file {} in DB....'.format(full_path))
    db.load_collection_from_json(full_path)

    print('After insertion: {}'.format(db.full_search().count()))
