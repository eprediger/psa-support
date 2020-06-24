from behave import given, when, then
from app import create_app, setup_database
<<<<<<< HEAD
from datetime import datetime, timedelta
=======
from settings import SEVERIDADES
>>>>>>> 6263d5c474785c64f4ed136e900472cb7caaaee6

app = create_app()
setup_database(app)
tc = app.test_client()

data_crear = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'pasos': None
}

data_editar = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
    'pasos': None,
    'estado': 'cerrado',
    'responsable': None
}

@given(u'The app is running')
def step_impl(context):
    print(u'STEP: Given The app is running')
    pass

<<<<<<< HEAD
@given(u'I am a help desk employee')
def step_impl(context):
    #print(u'STEP: Given I am a help desk employee')
    pass

# Criterio de aceptacion a)
@when(u'I ask to modify the ticket with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}", estado "{estado}", responsable "{responsable}", pasos "{pasos}"')
def step_impl(context, nombre, descripcion, tipo, severidad, estado, responsable, pasos):
    #print('STEP: When I ask to modify the ticket with nombre "{}", descripcion "{}", tipo "{}", severidad "{}", estado "{}", responsable "{}", pasos "{}"'.format(nombre, descripcion, tipo, severidad, estado, responsable, pasos))
    resp = context.tc.post('/tickets', json=data_crear)
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'responsable': responsable,
            'pasos': pasos,
            'estado': estado}
    resp = context.tc.put('/tickets/1', json=data)
    context.result = resp.get_json()['mensaje']

# Criterio de aceptacion e)
@when(u'I ask to modify the ticket with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}", estado from cerrado "{estado}", responsable "{responsable}", pasos "{pasos}"')
def step_impl(context, nombre, descripcion, tipo, severidad, estado, responsable, pasos):
    resp = context.tc.post('/tickets', json=data_crear)
    resp = context.tc.put('/tickets/1', json=data_editar)

    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'responsable': responsable,
            'pasos': pasos,
            'estado': estado}
    resp = context.tc.put('/tickets/1', json=data)
    context.result = resp.get_json()['mensaje']


@then(u'I get a message saying "{mensaje}"')
def step_impl(context, mensaje):
    #print(u'STEP: I get a message saying "{}"'.format(mensaje))
    assert context.result == mensaje


'''
# Criterio de aceptacion b1)
@when(u'I ask to modify the ticket "{id}" with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}", invalid estado "{estado}", responsable "{responsable}", pasos "{pasos}"')
def step_impl(context, id, nombre, descripcion, tipo, severidad, estado, responsable, pasos):
    print('STEP: When I ask to modify the ticket "{id}" with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}", invalid estado "{estado}", responsable "{responsable}", pasos "{pasos}"'.format(context, id, nombre, descripcion, tipo, severidad, estado, responsable, pasos))
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'responsable': responsable,
            'pasos': pasos,
            'estado': estado}
    resp = context.tc.put('/tickets/{}'.format(id), json=data)
    context.result = resp.get_json()['message']

# Criterio de aceptacion b2)
@when(u'I ask to modify the ticket "{id}" with nombre "{nombre}", descripcion "{descripcion}", invalid tipo "{tipo}", severidad "{severidad}", estado "{estado}", responsable "{responsable}", pasos "{pasos}"')
def step_impl(context, id, nombre, descripcion, tipo, severidad, estado, responsable, pasos):
    print('STEP: When I ask to modify the ticket "{id}" with nombre "{nombre}", descripcion "{descripcion}", invalid tipo "{tipo}", severidad "{severidad}", invalid estado "{estado}", responsable "{responsable}", pasos "{pasos}"'.format(context, id, nombre, descripcion, tipo, severidad, estado, responsable, pasos))
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'responsable': responsable,
            'pasos': pasos,
            'estado': estado}
    resp = context.tc.put('/tickets/{}'.format(id), json=data)
    context.result = resp.get_json()['message']

#criterio de aceptacion b3)
@when(u'I ask to modify the ticket "{id}" with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", invalid severidad "{severidad}", estado "{estado}", responsable "{responsable}", pasos "{pasos}"')
def step_impl(context, id, nombre, descripcion, tipo, severidad, estado, responsable, pasos):
    print('STEP: When I ask to modify the ticket "{id}" with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", invalid severidad "{severidad}", invalid estado "{estado}", responsable "{responsable}", pasos "{pasos}"'.format(context, id, nombre, descripcion, tipo, severidad, estado, responsable, pasos))
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'responsable': responsable,
            'pasos': pasos,
            'estado': estado}
    resp = context.tc.put('/tickets/{}'.format(id), json=data)
    context.result = resp.get_json()['message']

'''

#criterio de aceptacion c)
@when(u'I ask to modify the ticket with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}", estado cerrado "{estado}", responsable "{responsable}", pasos "{pasos}"')
def step_impl(context, nombre, descripcion, tipo, severidad, estado, responsable, pasos):
    #print('STEP: When I ask to modify the ticket with nombre "{}", descripcion "{}", tipo "{}", invalid severidad "{}", invalid estado "{}", responsable "{}", pasos "{}"'.format(nombre, descripcion, tipo, severidad, estado, responsable, pasos))
    resp = context.tc.post('/tickets', json=data_crear)
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'responsable': responsable,
            'pasos': pasos,
            'estado': estado}
    resp = context.tc.put('/tickets/1', json=data)
    
    resp = context.tc.get('/tickets')
    fecha_finalizacion = resp.get_json()['tickets'][0]['fecha_finalizacion']
    context.result = datetime.strptime(fecha_finalizacion, '%Y-%m-%d %H:%M:%S').date()

@then(u"The fecha finalizacion will be the today's date")
def step_impl(context):
    assert context.result == datetime.today().date()


#criterio de aceptacion d)
@when(u'I ask to modify the ticket with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", new severidad "{severidad}", estado "{estado}", responsable "{responsable}", pasos "{pasos}"')
def step_impl(context, nombre, descripcion, tipo, severidad, estado, responsable, pasos):
    resp = context.tc.post('/tickets', json=data_crear)
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'responsable': responsable,
            'pasos': pasos,
            'estado': estado}
    resp = context.tc.put('/tickets/1', json=data)

    print(resp.get_json())

    resp = context.tc.get('/tickets')

    print(resp.get_json())

    fecha_limite = resp.get_json()['tickets'][0]['fecha_limite']
    context.result = datetime.strptime(fecha_limite, '%Y-%m-%d %H:%M:%S').date()


@then(u'The fecha limite will be updated with the today s date plus "{dias}" days')
def step_impl(context, dias):
    fecha_limite = (datetime.today() + timedelta(days=int(dias))).date()
    print(' A VER', context.result, fecha_limite )
    assert context.result == fecha_limite


@when(u'I ask to view all the tickets and they don t exists')
def step_impl(context):
    print(u'STEP: When ask to view all the tickets')
    resp = context.tc.get('/tickets')
    context.result = resp.get_json()['tickets']
=======

@given(u'I am an Analista de mesa de ayuda')
def step_impl(context):
    print(u'STEP: Given I am an Analista de mesa de ayuda')
    pass
>>>>>>> 6263d5c474785c64f4ed136e900472cb7caaaee6

@when(u'I ask to view all the tickets')
def step_impl(context):
    print(u'STEP: When ask to view all the tickets')
    resp = context.tc.post('/tickets', json=data_crear)
    resp = context.tc.get('/tickets')
    context.result = resp.get_json()['tickets']

@then(u'I receive an empty list of tickets')
def step_impl(context):
    print(u'STEP: Then I receive an empty list of tickets')
    assert context.result == []

<<<<<<< HEAD
@then(u'I receive a list of tickets')
def step_impl(context):
    print(u'STEP: Then I receive an empty list of tickets')
    assert len(context.result)>0

@then(u'I get the ticket with an id "{id}" of the database')
def step_impl(context, id):
    print(u'STEP: I get the ticket with an id "{}" of the database'.format(id))
    assert context.result == int(id)

=======
@when(u'I create a ticket with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}"')
def step_impl(context, nombre, descripcion, tipo, severidad):
    print(u'STEP: When I create a ticket with nombre "{}", descripcion "{}", tipo "{}", severidad "{}"'.format(nombre, descripcion, tipo, severidad))
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion}
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
            'descripcion': descripcion}
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
>>>>>>> 6263d5c474785c64f4ed136e900472cb7caaaee6
