from behave import given, when, then
from app import create_app, setup_database
from datetime import datetime, timedelta
from settings import SEVERIDADES

app = create_app()
setup_database(app)
tc = app.test_client()

data_crear = {
    'nombre': 'test',
    'descripcion': 'test',
    'severidad': 'alta',
    'tipo': 'consulta',
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
    resp = context.tc.get('/tickets')

    fecha_limite = resp.get_json()['tickets'][0]['fecha_limite']
    context.result = datetime.strptime(fecha_limite, '%Y-%m-%d %H:%M:%S').date()


@then(u'The fecha limite will be updated with the today s date plus "{dias}" days')
def step_impl(context, dias):
    fecha_limite = (datetime.today() + timedelta(days=int(dias))).date()
    print(' A VER', context.result, fecha_limite )
    assert context.result == fecha_limite