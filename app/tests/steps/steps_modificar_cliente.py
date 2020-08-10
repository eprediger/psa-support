from datetime import datetime, timedelta

from behave import given, then, when

from app.main.settings import SEVERIDADES

cliente_creado = {
    'razon_social' : "razon social prueba",
    'CUIT' : "123456",
    'descripcion' : "descripcion prueba"
}

modificaciones_cliente = {
    'razon_social' : "razon social 2",
    'CUIT' : "654321",
    'descripcion' : "descripcion modificada",
    'estado': 'activo'
}


@given(u'I am an Analista de mesa de ayuda and i have a client with razon social: "razon social prueba", CUIT:"123456", descripcion:"descripcion prueba"')
def step_impl(context):
    context.tc.post('/clientes', json=cliente_creado)


@when(u'I modify the razon social por "razon social 2", CUIT:"654321", descripcion: "descripcion modificada"')
def step_impl(context):
    context.tc.put('/clientes/1', json=modificaciones_cliente)

@then(u'I can see a cliente With CUIT "{CUIT}" and the rest of its atributes modified.')
def step_impl(context, CUIT):
    resp =  context.tc.get('/clientes').get_json()[0]['CUIT']
    print(resp)
    assert resp == CUIT

@when(u'I modify the razon social por "", CUIT:"", descripcion: ""')
def step_impl(context):
    data = {
        'razon_social' : None,
        'CUIT' : None,
        'descripcion' : None
    }
    resp = context.tc.put('/clientes/1', json=data)
    context.result = resp.get_json()['mensaje']

@then(u'I can see the cliente asigned to the ticket With CUIT "654321" and the rest of its atributes modified.')
def step_impl(context):
    resp = context.tc.get('/tickets').get_json()[0]['cliente']
    print(resp)
    assert resp['CUIT'] == "654321"
