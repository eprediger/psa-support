# -- FILE: features/environment.py
# flaskr is the sample application we want to test
import os
import tempfile

from behave import given

#Fiddly
#fuente: https://stackoverflow.com/questions/33067785/bdd-behave-selenium-python-error-no-module-named-pages-when-i-run-my-feature-tes
import imp
app = imp.load_source('app', '../app.py')
from app import create_app

config = imp.load_source('config', '../main/config.py')
from config import config

#from ..app import create_app
#from ..main.config import config


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
