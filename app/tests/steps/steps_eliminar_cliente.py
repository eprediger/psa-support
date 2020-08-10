from datetime import datetime, timedelta

from behave import given, then, when

from app.main.settings import SEVERIDADES

ticket_crear = {
    'nombre': 'test',
    'descripcion': 'test de descripcion',
    'severidad': 'alta',
    'tipo': 'consulta',
    'cliente': {'id': None}
}

@given(u'I have a client with razon social: "{razon_social}", CUIT:"{CUIT}", descripcion:"{descripcion}"')
def step_impl(context,razon_social,descripcion,CUIT):
    data = {
        'razon_social' : razon_social,
        'descripcion' : descripcion,
        'CUIT' : CUIT
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
    total_clientes = len(context.tc.get('/clientes').get_json())
    print("En total hay: ",total_clientes)


@when(u'I delete the client 1')
def step_impl(context):
    resp = context.tc.delete('/clientes/1').get_json()['mensaje']
    context.result = resp


@then(u'I can see a warning saying that the client doesnt exist')
def step_impl(context):
    assert context.result == "No existe el cliente solicitado"

@given(u'I have a client with razon social: "{razon_social}", CUIT:"{CUIT}", descripcion:"{descripcion}" ready to delete')
def step_impl(context, razon_social, CUIT, descripcion):
    data = {
        'razon_social' : razon_social,
        'descripcion' : descripcion,
        'CUIT' : CUIT
    }
    context.tc.post('/clientes',json=data)
    context.tc.post('/tickets', json=ticket_crear)
    id_cliente = context.tc.get('/clientes').get_json()[0]['id']
    ticket = context.tc.get('/tickets').get_json()[0]
    ticket['cliente'] = {'id': id_cliente}
    context.tc.put('/tickets/1', json = ticket)
    print(u'{}'.format(context.tc.get('/tickets').get_json()[0]))

@then(u'I can see a warning saying that the client cant be deleted because its asigned to a ticket')
def step_impl(context):
    print(context.tc.get('/tickets').get_json()[0])
    print(context.result)
    assert context.result == "No se puede eliminar el cliente solicitado ya que está asignado a un ticket"
