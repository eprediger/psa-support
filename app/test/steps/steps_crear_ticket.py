from datetime import datetime, timedelta

from behave import given, then, when

from settings import SEVERIDADES


@when(u'I create a ticket with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}"')
def step_impl(context, nombre, descripcion, tipo, severidad):
    print(u'STEP: When I create a ticket with nombre "{}", descripcion "{}", tipo "{}", severidad "{}"'.format(nombre, descripcion, tipo, severidad))
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'cliente': {'id': None}
        }
    resp = context.tc.post('/tickets', json=data)

    if severidad not in SEVERIDADES.keys() or tipo not in ['error', 'consulta', 'mejora']:
        context.result = resp.get_json()['mensaje']
    else:
        context.result = resp.get_json()['estado']

@then(u'a ticket is created with estado "{estado}"')
def step_impl(context, estado):
    print(u'STEP: Then a ticket is created with estado "{}"'.format(estado))
    assert context.result == "nuevo"

@when(u'I create a ticket with descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}"')
def step_impl(context, descripcion, tipo, severidad):
    print(u'STEP: When I create a ticket with descripcion "{}", tipo "{}", severidad "{}"'.format(descripcion, tipo, severidad))
    data = {'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'cliente': {'id': None}}
    resp = context.tc.post('/tickets', json=data)
    context.result = resp.get_json()['mensaje']

@then(u'I recive a warning because there is information that is missing')
def step_impl(context):
    print(u'STEP: Then I recive a warning because there is information that is missing')
    assert context.result == "Parametros invalidos"

@then(u'I recive a warning because there is a wrong value at severidad')
def step_impl(context):
    print(u'STEP: Then I recive a warning because there is a wrong value at severidad')
    assert context.result == "La severidad debe ser Alta, Media o Baja"

@then(u'I recive a warning because there is a wrong value at tipo')
def step_impl(context):
    print(u'STEP: Then I recive a warning because there is a wrong value at tipo')
    assert context.result == "El tipo de ticket debe ser Error/Consulta/Mejora"
