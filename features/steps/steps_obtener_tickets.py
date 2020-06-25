from behave import given, when, then
from app import create_app, setup_database
from datetime import datetime, timedelta
from settings import SEVERIDADES


data_crear = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'pasos': None
}

@when(u'I ask to view all the tickets and they don t exists')
def step_impl(context):
    print(u'STEP: When ask to view all the tickets')
    resp = context.tc.get('/tickets')
    context.result = resp.get_json()['tickets']


@when(u'I ask to view all the tickets')
def step_impl(context):
    print(u'STEP: When ask to view all the tickets')
    resp = context.tc.post('/tickets', json=data_crear)
    resp = context.tc.get('/tickets')
    context.result = resp.get_json()['tickets']


@then(u'I receive an empty list of tickets')
def step_impl(context):
    print(u'STEP: Then I receive an empty list of tickets')
    assert context.result == []


@then(u'I receive a list of tickets')
def step_impl(context):
    print(u'STEP: Then I receive an empty list of tickets')
    assert len(context.result)>0
