from behave import given, when, then
from app import create_app, setup_database
from datetime import datetime, timedelta
from settings import SEVERIDADES

ticket_crear = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'pasos': None,
    'cliente_asignado' : 'Cliente Inicial'
}

cliente_a_asignar = {
    "descripcion": "Area logistica de Test",
    "razon_social": "Cliente Asignado Test S.A.",
    "CUIT": "33-654321-5",
    "fecha_desde_que_es_cliente": "Wed, 10 Jul 2019 16:58:55 GMT"
}

cliente_a_modificar = {
    "descripcion": "Area logistica de Test",
    "razon_social": "Test S.A.",
    "CUIT": "33-654321-5",
    "fecha_desde_que_es_cliente": "Wed, 10 Jul 2019 16:58:55 GMT"
}

@given(u'I have a client and a ticket that already has a client loaded')
def step_impl(context):
    context.tc.post('/tickets', json = ticket_crear)
    context.tc.post('/clientes', json = cliente_a_asignar)
    context.tc.post('/clientes', json = cliente_a_modificar)
    cliente = context.tc.get('/clientes').get_json()['clientes'][0]['razon_social']
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['cliente_asignado'] = cliente
    context.tc.put('/tickets/1', json=ticket)


@when(u'I modify the client of the ticket')
def step_impl(context):
    cliente = context.tc.get('/clientes').get_json()['clientes'][1]['razon_social']
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['cliente_asignado'] = cliente
    context.tc.put('/tickets/1', json=ticket)


@then(u'I can see the name of the new client asigned to the ticket')
def step_impl(context):
    assert context.tc.get('/tickets').get_json()['tickets'][0]['cliente_asignado'] == "Test S.A."

@given(u'I ticket that already has a client loaded')
def step_impl(context):
    context.tc.post('/tickets', json = ticket_crear)
    context.tc.post('/clientes', json = cliente_a_asignar)
    cliente = context.tc.get('/clientes').get_json()['clientes'][0]['razon_social']
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['cliente_asignado'] = cliente

@when(u'I modify the client of the ticket with another that doesnt exist')
def step_impl(context):
    cliente = {}
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['cliente_asignado'] = None
    resp = context.tc.put('/tickets/1', json=None)
    context.result = resp