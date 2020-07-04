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

@given(u'I have a ticket that already has a client loaded')
def step_impl(context):
    context.tc.post('/tickets', json = ticket_crear)
    context.tc.post('/clientes', json = cliente_a_asignar)
    cliente = context.tc.get('/clientes').get_json()['clientes'][0]['id']
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['id'] = cliente
    context.tc.put('/tickets/1', json=ticket)


@when(u'I delete the client of the ticket')
def step_impl(context):
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['id'] = None
    context.tc.put('/tickets/1', json=ticket)


@then(u'I can see that the ticket has no client asigned')
def step_impl(context):
    resp = context.tc.get('/tickets').get_json()['tickets'][0]
    assert resp['cliente'] == None
