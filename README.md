# MolSSI API (Flask)

This application is the MolSSI API server for the molecular sciences software resources.

The server runs Flask on Passenger and Apache.

### Run the Development Web Server
Create a virtual environment and start the local app.

```
# If you have anaconda as your default, make sure to run
conda install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python molssi_api_flask.py