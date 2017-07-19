import sys, os
INTERP = os.path.join(os.environ['HOME'], 'api.molssi.org', 'venv', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())


sys.path.append('app')
from molssi_api_flask import app as application
