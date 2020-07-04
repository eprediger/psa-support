from behave import given, when, then
from app import create_app, setup_database
from datetime import datetime, timedelta
from settings import SEVERIDADES

ticket_crear = {
    'nombre': 'test',
    'descripcion': 'test de descripcion',
    'severidad': 'alta',
    'tipo': 'consulta',
}

@given(u'I have a client with razon social: "{razon_social}", CUIT:"{CUIT}", descripcion:"{descripcion}", fecha desde que es cliente:"{fecha_desde_que_es_cliente}"')
def step_impl(context,razon_social,descripcion,CUIT,fecha_desde_que_es_cliente):
    data = {
        'razon_social' : razon_social,
        'descripcion' : descripcion,
        'CUIT' : CUIT,
        'fecha_desde_que_es_cliente' : fecha_desde_que_es_cliente
    }
    context.tc.post('/clientes',json=data)


@when(u'I delete the client')
def step_impl(context):
    resp = context.tc.delete('/clientes/1').get_json()['mensaje']
    context.result = resp


@then(u'I can see a message saying that the client was deleted succesfully')
def step_impl(context):
    print(context.result)
    assert context.result == "Cliente eliminado con exito!"

@given(u'I have no clients')
def step_impl(context):
    total_clientes = len(context.tc.get('/clientes').get_json()['clientes'])
    print("En total hay: ",total_clientes)


@when(u'I delete the client 1')
def step_impl(context):
    resp = context.tc.delete('/clientes/1').get_json()['mensaje']
    context.result = resp


@then(u'I can see a warning saying that the client doesnt exist')
def step_impl(context):
    assert context.result == "No existe el cliente solicitado"

@given(u'I have a client with razon social: "{razon_social}", CUIT:"{CUIT}", descripcion:"{descripcion}", fecha desde que es cliente:"{fecha_desde_que_es_cliente}" asigned to a ticket')
def step_impl(context, razon_social, CUIT, descripcion, fecha_desde_que_es_cliente):
    data = {
        'razon_social' : razon_social,
        'descripcion' : descripcion,
        'CUIT' : CUIT,
        'fecha_desde_que_es_cliente' : fecha_desde_que_es_cliente
    }
    context.tc.post('/clientes',json=data)    
    context.tc.post('/tickets', json=ticket_crear)
    id_cliente = context.tc.get('/clientes').get_json()['clientes'][0]['id']
    ticket = context.tc.get('/tickets').get_json()['tickets'][0]
    ticket['id_cliente'] = id_cliente
    context.tc.put('/tickets/1', json = ticket)
    print(u'{}'.format(context.tc.get('/tickets').get_json()['tickets'][0]))

@then(u'I can see a warning saying that the client cant be deleted because its asigned to a ticket')
def step_impl(context):
    print(context.tc.get('/tickets').get_json()['tickets'][0])
    print(context.result)
    assert context.result == "No se puede eliminar el cliente solicitado ya que está asignado a un ticket"