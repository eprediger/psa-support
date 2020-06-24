# -- FILE: features/environment.py
# flaskr is the sample application we want to test
from app import create_app, setup_database

import os
import tempfile

def before_scenario(context, feature):
    # -- HINT: Recreate a new flaskr client before each feature is executed.
    app = create_app()
    #context.db, app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True
    context.tc = app.test_client()
    setup_database(app)
    #os.close(context.db)
    #os.unlink(app.config['DATABASE'])