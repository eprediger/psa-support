from behave import given, when, then
from app import create_app, setup_database
from datetime import datetime, timedelta
from settings import SEVERIDADES

ticket_crear = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'pasos': None
}

cliente_a_asignar = {
    "descripcion": "Area logistica de Test",
    "razon_social": "Test S.A.",
    "CUIT": "33-654321-5",
    "fecha_desde_que_es_cliente": "Wed, 10 Jul 2019 16:58:55 GMT"
}

@given(u'I have a client and a ticket')
def step_impl(context):
    print(u'STEP: Given I have a client and a ticket')
    context.tc.post('/tickets', json=ticket_crear)
    context.tc.post('/clientes', json=cliente_a_asignar)


@when(u'I asign the client to the ticket')
def step_impl(context):
    cliente = context.tc.get('/clientes').get_json()['clientes'][0]['razon_social']
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['cliente_asignado'] = cliente
    resp = context.tc.put('/tickets/1', json=ticket)
    context.result = resp


@then(u'I can see the name of the client asigned to the ticket')
def step_impl(context):
    print(context.tc.get('/tickets').get_json()['tickets'][0]['cliente_asignado'])
    assert context.tc.get('/tickets').get_json()['tickets'][0]['cliente_asignado'] == "Test S.A."

@given(u'I have a ticket')
def step_impl(context):
    print(u'STEP: Given I have a ticket')
    context.tc.post('/tickets', json=ticket_crear)

@when(u'I asign an unexisting client to the ticket')
def step_impl(context):
    print(u'STEP: When I asign an unexisting client to the ticket')
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    resp = context.tc.put('/tickets/1', json=None)
    context.result = resp

@then(u'I can see a warning because the client doesnt exist')
def step_impl(context):
    print(u'STEP: Then I can see a warning because the client doesnt exist')
    assert context.result.get_json()['mensaje'] == 'Parametros invalidos'