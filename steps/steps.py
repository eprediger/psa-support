from behave import given, when, then
from app import create_app, setup_database

app = create_app()
setup_database(app)
tc = app.test_client()

@given(u'The app is running')
def step_impl(context):
    print(u'STEP: Given The app is running')
    pass

@when(u'I ask to view all the tickets')
def step_impl(context):
    print(u'STEP: When ask to view all the tickets')
    resp = tc.get('/tickets')
    context.result = resp.get_json()['tickets']

@then(u'I receive an empty list of tickets')
def step_impl(context):
    print(u'STEP: Then I receive an empty list of tickets')
    assert context.result == []

@when(u'I ask to create a ticket with nombre "{nombre}", descripcion "{descripcion}", tipo "{tipo}", severidad "{severidad}", fecha de creacion "{fecha_creacion}", fecha de actualizacion "{fecha_ultima_actualizacion}", estado "{estado}"')
def step_impl(context, nombre, descripcion, tipo, severidad, fecha_creacion, fecha_ultima_actualizacion, estado):
    print(u'STEP: When I ask to create a ticket with nombre "{}", descripcion "{}", tipo "{}", severidad "{}", fecha de creacion "{}", fecha de actualizacion "{}", estado "{}"'.format(nombre, descripcion, tipo, severidad, fecha_creacion, fecha_ultima_actualizacion, estado))
    data = {'nombre': nombre,
            'tipo': tipo,
            'severidad': severidad,
            'descripcion': descripcion,
            'fecha_creacion': fecha_creacion,
            'fecha_ultima_actualizacion': fecha_ultima_actualizacion,
            'estado': estado}
    resp = tc.post('/tickets', json=data)
    context.result = resp.get_json()['id']

@then(u'I get the ticket with an id "{id}" of the database')
def step_impl(context, id):
    print(u'STEP: I get the ticket with an id "{}" of the database'.format(id))
    assert context.result == int(id)
