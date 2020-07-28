# -- FILE: features/environment.py
# flaskr is the sample application we want to test
import os
import tempfile

from behave import given

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from app import create_app
from main.config import config


@given(u'I am an Analista de mesa de ayuda')
def step_impl(context):
    print(u'STEP: Given I am an Analista de mesa de ayuda')
    pass


def before_scenario(context, feature):
    environment = config['featureTest']
    # -- HINT: Recreate a new flaskr client before each feature is executed.
    app = create_app(environment)
    #context.db, app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True
    context.tc = app.test_client()
    #os.close(context.db)
    #os.unlink(app.config['DATABASE'])
