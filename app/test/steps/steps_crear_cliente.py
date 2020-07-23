from datetime import datetime, timedelta

from behave import given, then, when

from settings import SEVERIDADES


@when(u'I create a client with razon social:"{razon_social}", descripcion:"{descripcion}", CUIT:"{CUIT}", fecha desde que es cliente:"{fecha_desde_que_es_cliente}"')
def step_impl(context, razon_social, descripcion, CUIT, fecha_desde_que_es_cliente):
    data = {
        'razon_social' : razon_social,
        'descripcion' : descripcion,
        'CUIT' : CUIT,
        'fecha_desde_que_es_cliente' : fecha_desde_que_es_cliente
    }
    context.tc.post('/clientes', json=data)
    resp = context.tc.get('/clientes').get_json()[0]['CUIT']
    context.result = resp

@then(u'a client is created with a CUIT:"{CUIT}"')
def step_impl(context, CUIT):
    assert context.result == CUIT

@when(u'I create a client without razon social:"razon social prueba", descripcion:"descripcion prueba", CUIT:"12345654", fecha desde que es cliente:"12022020"')
def step_impl(context):
    data = {
        'razon_social' : None,
        'descripcion' : None,
        'CUIT' : None,
        'fecha_desde_que_es_cliente' : None
    }
    resp = context.tc.post('/clientes', json=data)
    context.result = resp.get_json()['mensaje']

@then(u'I see a warning that all the fields must be filled.')
def step_impl(context):
    assert context.result == "Parametros invalidos"
