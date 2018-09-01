[![Build Status](https://travis-ci.org/doaa-altarawy/molssi_api_flask.svg?branch=master)](https://travis-ci.org/doaa-altarawy/molssi_api_flask)
[![codecov](https://codecov.io/gh/doaa-altarawy/molssi_api_flask/branch/master/graph/badge.svg)](https://codecov.io/gh/doaa-altarawy/molssi_api_flask)

# MolSSI API (Flask)

This application is the MolSSI API server for the molecular sciences software resources.

The server runs Flask on Passenger and Apache.

## Setup the mongo DB (for developement only)

For Ubunut:

`sudo apt-get install mongodb`

For macOS:

```
sudo brew install mongodb
sudo mkdir -p /data/db
sudo chmod 777 /data/db   # or add the DB user to the group

brew services start mongodb # start the service
```


To run the DB service:

`$ mongod`
Or if using a different path than the default /data/db:
`$mongod --dbpath <path to data directory>`


### Create Mongo DBs and a user:
```
$ mongo
> use resources_website
> db.createUser({user: 'doaa', pwd: 'fakePass', roles : [{db: 'resources_website', role: 'readWrite'}] } )
> quit()   # save and exit

# fill the database with sameple data:
$ mongoimport --db resources_website --collection software --type json --jsonArray --file molssi_code_db/tests/data/software.json
$ mongoimport --db test_db --collection software --type json --jsonArray --file molssi_code_db/tests/data/software.json

```

### Run the Development Web Server
Create a virtual environment and start the local app.

```
# If you have anaconda as your default, make sure to run
git clone https://github.com/doaa-altarawy/molssi_api_flask.git
cd molssi_api_flask
conda install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python molssi_api_flask.py
```