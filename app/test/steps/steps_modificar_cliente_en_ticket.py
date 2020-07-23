from datetime import datetime, timedelta

from behave import given, then, when

from settings import SEVERIDADES

ticket_crear = {
    'nombre': 'test',
    'descripcion': 'test de descripcion',
    'severidad': 'alta',
    'tipo': 'consulta',
    'cliente': {'id': None}
}

cliente_a_asignar = {
    "descripcion": "Area logistica de Test1",
    "razon_social": "Cliente Asignado Test1 S.A.",
    "CUIT": "12-456-5",
    "fecha_desde_que_es_cliente": "Wed, 10 Jul 2016 16:58:55 GMT"
}

cliente_a_modificar = {
    "descripcion": "Area logistica de Test2",
    "razon_social": "Test2 S.A.",
    "CUIT": "33-654321-5",
    "fecha_desde_que_es_cliente": "Wed, 10 Jul 2019 16:58:55 GMT"
}

@given(u'I have a client and a ticket that already has a client loaded')
def step_impl(context):
    context.tc.post('/tickets', json = ticket_crear)
    context.tc.post('/clientes', json = cliente_a_asignar)
    context.tc.post('/clientes', json = cliente_a_modificar)
    id_cliente = context.tc.get('/clientes').get_json()[0]['id']
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['cliente'] = {'id': id_cliente}
    context.tc.put('/tickets/1', json=ticket)


@when(u'I change the client of the ticket')
def step_impl(context):
    id_cliente = context.tc.get('/clientes').get_json()[1]['id']
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['cliente'] = {'id': id_cliente}
    context.tc.put('/tickets/1', json=ticket)


@then(u'I can see the name of the new client asigned to the ticket')
def step_impl(context):
    assert context.tc.get('/tickets').get_json()[0]['cliente']['razon_social'] == "Test2 S.A."

@given(u'I ticket that already has a client loaded')
def step_impl(context):
    context.tc.post('/tickets', json = ticket_crear)
    context.tc.post('/clientes', json = cliente_a_asignar)
    cliente = context.tc.get('/clientes').get_json()[0]['razon_social']
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['cliente_asignado'] = cliente

@when(u'I change the client of the ticket with another that doesnt exist')
def step_impl(context):
    cliente = {}
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['cliente_asignado'] = None
    resp = context.tc.put('/tickets/1', json=None)
    context.result = resp
