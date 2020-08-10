from datetime import datetime, timedelta

from behave import given, then, when

from app.main.settings import SEVERIDADES

ticket_crear = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'pasos': None,
    'cliente': {'id': None}
}

cliente_a_asignar = {
    "descripcion": "Area logistica de Test",
    "razon_social": "Cliente Asignado Test S.A.",
    "CUIT": "33-654321-5"
}

@given(u'I have a ticket that already has a client loaded')
def step_impl(context):
    context.tc.post('/tickets', json = ticket_crear)
    context.tc.post('/clientes', json = cliente_a_asignar)
    cliente = context.tc.get('/clientes').get_json()[0]['id']
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['id'] = cliente
    context.tc.put('/tickets/1', json=ticket)


@when(u'I delete the client of the ticket')
def step_impl(context):
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['id'] = None
    context.tc.put('/tickets/1', json=ticket)


@then(u'I can see that the ticket has no client asigned')
def step_impl(context):
    resp = context.tc.get('/tickets').get_json()[0]
    assert resp['cliente'] == None
