from __future__ import print_function
from molssi_api_flask.core import mongo_database as db
import os
import config as config

#  MongoDB connection
db.get_connection(config.DB_URI)
print('Connecting to DB: ', config.DB_URI)

#  Clear the DB
db.clear_libraries()

# Files to be loaded into the DB
# files = ['wiki_QM.json', 'wiki_MM.json']
MM_files = ['MM_curated_data.json']
QM_files = ['QM_curated_data.json']


print('Initial DB size: {}'.format(db.full_search().count()))
for filename in MM_files:
    full_path = os.path.join(config.APPLICATION_ROOT, 'data', filename)
    print('Loading file {} in DB....'.format(full_path))
    db.load_collection_from_json(full_path)

    print('After insertion: {}'.format(db.full_search().count()))

for filename in QM_files:
    full_path = os.path.join(config.APPLICATION_ROOT, 'data', filename)
    print('Loading file {} in DB....'.format(full_path))
    db.load_collection_from_json(full_path)

    print('After insertion: {}'.format(db.full_search().count()))
