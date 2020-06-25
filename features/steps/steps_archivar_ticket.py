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

data_editar = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'pasos': None,
    'estado': 'cerrado',
    'responsable': None
}


@when(u'I ask to Archive an existing ticket')
def step_impl(context):
    resp = context.tc.post('/tickets', json=data_crear)
    resp = context.tc.put('/tickets/1', json=data_editar)
    resp = context.tc.delete('/tickets/1')
    context.result = resp.get_json()['mensaje']


@when(u'I ask to Archive an existing ticket with estado not cerrado')
def step_impl(context):
    resp = context.tc.post('/tickets', json=data_crear)
    resp = context.tc.delete('/tickets/1')
    context.result = resp.get_json()['mensaje']
