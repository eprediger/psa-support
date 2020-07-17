from datetime import datetime, timedelta

from behave import given, then, when

from settings import SEVERIDADES

ticket_crear = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'cliente': {'id': None}
}

cliente_a_asignar = {
    "descripcion": "Area logistica de Test",
    "razon_social": "Test S.A.",
    "CUIT": "33-654321-5"
}

@given(u'I have a client and a ticket')
def step_impl(context):
    print(u'STEP: Given I have a client and a ticket')
    context.tc.post('/tickets', json=ticket_crear)
    context.tc.post('/clientes', json=cliente_a_asignar)


@when(u'I asign the client to the ticket')
def step_impl(context):
    id_cliente = context.tc.get('/clientes').get_json()[0]['id']
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['cliente'] = {'id': id_cliente}
    resp = context.tc.put('/tickets/1', json=ticket)
    context.result = resp


@then(u'I can see the name of the client asigned to the ticket')
def step_impl(context):
    print(context.tc.get('/tickets').get_json()[0]['cliente'])
    assert context.tc.get('/tickets').get_json()[0]['cliente']['razon_social'] == "Test S.A."

@given(u'I have a ticket')
def step_impl(context):
    print(u'STEP: Given I have a ticket')
    context.tc.post('/tickets', json=ticket_crear)

@when(u'I asign an unexisting client to the ticket')
def step_impl(context):
    print(u'STEP: When I asign an unexisting client to the ticket')
    ticket = context.tc.get('/tickets').get_json()[0]
    resp = context.tc.put('/tickets/1', json=None)
    context.result = resp

@then(u'I can see a warning because the client doesnt exist')
def step_impl(context):
    print(u'STEP: Then I can see a warning because the client doesnt exist')
    assert context.result.get_json()['mensaje'] == 'Parametros invalidos'
