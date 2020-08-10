from datetime import datetime, timedelta, date
from pytz import timezone
from random import randint, uniform,random
from sqlalchemy import func, cast, Date

from app.main.db.database import (db, agregar_instancia, editar_instancia,
                              eliminar_instancia,
                              obtener_instancias_por_filtro,
                              obtener_todas_las_instancias,
                              obtener_una_instancia)
from app.main.models.Ticket import Ticket
from app.main.settings import SEVERIDADES


def obtener_tickets(query_params):
	tickets = []

	if query_params:
		tickets = obtener_instancias_por_filtro(Ticket, **query_params)
	else:
		tickets = obtener_todas_las_instancias(Ticket, "fecha_creacion")

	return [t.a_diccionario() for t in tickets]

def obtener_ticket_por(id):
	ticket = obtener_una_instancia(Ticket, id=id)

	return ticket.a_diccionario(incluir_tareas=True)

def crear(ticket):
	tipo = ticket['tipo'].lower()
	if tipo not in ['error', 'consulta', 'mejora']:
		raise Exception('El tipo de ticket debe ser Error/Consulta/Mejora')

	severidad = ticket['severidad'].lower()
	if severidad not in SEVERIDADES.keys():
		raise Exception("La severidad debe ser Alta, Media o Baja")

	id_cliente = ticket['cliente']['id']

	fecha_creacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))
	fecha_limite = fecha_creacion + timedelta(days=SEVERIDADES[severidad])

	ticket = agregar_instancia(Ticket, nombre=ticket['nombre'],
						descripcion=ticket['descripcion'],
						tipo=tipo,
						severidad=severidad,
						fecha_creacion=fecha_creacion,
						fecha_limite=fecha_limite,
						fecha_ultima_actualizacion=fecha_creacion,
						pasos=ticket.get('pasos'),
						id_cliente=id_cliente,
						legajo_responsable=ticket.get('legajo_responsable'))

	return ticket.a_diccionario()

def editar(id, ticket_editado):

	ticket_almacenado = obtener_una_instancia(Ticket, id=id)

	if not ticket_almacenado:
		raise Exception("No existe el ticket solicitado")

	id_cliente = ticket_editado['cliente']['id']

	pasos = ticket_editado.get('pasos')
	responsable = ticket_editado.get('legajo_responsable')

	estado = ticket_editado['estado'].lower()

	if ticket_almacenado.estado == 'cerrado':
		raise Exception('El ticket ya fue cerrado previamente')

	if estado not in ['nuevo', 'en progreso', 'cerrado', 'esperando informacion']:
		raise Exception('El estado de ticket debe ser Nuevo/Asignado/Cerrado/Esperando Informacion')
	# , CODIGO_HTTP["BAD_REQUEST"]

	fecha_ultima_actualizacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))

	if estado == 'cerrado' and ticket_almacenado.estado != 'cerrado':
		# Si cambio al estado cerrado, se coloca la fecha de finalización.
		fecha_finalizacion = fecha_ultima_actualizacion
	else:
		fecha_finalizacion = None

	severidad = ticket_editado['severidad'].lower()
	if severidad not in SEVERIDADES.keys():
		raise Exception('La severidad debe ser Alta, Media o Baja')

	if severidad != ticket_almacenado.severidad:
		# Si cambiaron la severidad del ticket, se actualiza la fecha limite.
		fecha_limite = ticket_almacenado.fecha_creacion + timedelta(days=SEVERIDADES[severidad.lower()])
	else:
		fecha_limite = ticket_almacenado.fecha_limite

	tipo = ticket_editado['tipo'].lower()

	if tipo not in ['error', 'consulta', 'mejora']:
		raise Exception('El tipo de ticket debe ser Error/Consulta/Mejora')
	# , CODIGO_HTTP["BAD_REQUEST"]

	if tipo != 'error':
		# Solo los tickets de tipo error llevan pasos
		pasos = None

#Codigo para la creacion de tickets que den datos a los graficos
	try:
		fecha_creacion = ticket_editado['fecha_creacion']
		fecha_creacion = datetime.strptime(fecha_creacion, '%Y-%m-%d %H:%M:%S')
	except:
		fecha_creacion = None

	try:
		fecha_finalizacion = ticket_editado['fecha_finalizacion']
		fecha_finalizacion = datetime.strptime(fecha_finalizacion, '%Y-%m-%d %H:%M:%S')
	except:
		pass

	editar_instancia(Ticket, id,
						nombre=ticket_editado["nombre"],
						descripcion=ticket_editado["descripcion"],
						tipo=tipo,
						estado=estado,
						severidad=severidad,
						fecha_ultima_actualizacion=fecha_ultima_actualizacion,
						fecha_limite=fecha_limite,
						fecha_finalizacion=fecha_finalizacion,
						legajo_responsable=responsable,
						pasos=pasos,
						fecha_creacion=fecha_creacion,
						id_cliente=id_cliente)
# Fin de codigo para la creacion de tickets que den datos a los graficos

def archivar(id):
	ticket = obtener_una_instancia(Ticket, id=id)

	if not ticket:
		raise Exception('No existe el ticket solicitado')
	# , CODIGO_HTTP["NOT_FOUND"]

	if ticket.estado.lower() != 'cerrado':
		raise Exception('Los tickets deben estar cerrados para poder archivarse!')
	# , CODIGO_HTTP["BAD_REQUEST"]

	eliminar_instancia(Ticket, id=id)

def completar_ceros(tickets):
	if len(tickets) > 0:
		fechaInicio = tickets[0]["fecha"]
		fechaFin = date.today()
		delta = fechaFin - fechaInicio

		for i in range(delta.days + 1):
			dia = fechaInicio + timedelta(days=i)
			diaString = dia.strftime("%Y-%m-%d")
			if diaString not in [ ticket['fecha'].strftime("%Y-%m-%d") for ticket in tickets ]:
				tickets.append({'fecha': diaString, 'cantidad': 0})

		tickets.sort(key=lambda x: x["fecha"])

	return tickets

def obtener_data_diaria():
	query = """SELECT date(fecha_finalizacion), count(*)
			FROM tickets
			WHERE date(fecha_finalizacion) is not null
			GROUP BY date(fecha_finalizacion);"""

	tickets_cerrados = db.engine.execute(query)
	tickets_cerrados = [{'fecha': tc[0], 'cantidad': tc[1]} for tc in tickets_cerrados]
	tickets_cerrados = completar_ceros(tickets_cerrados)


	query = """SELECT date(fecha_creacion), count(*)
			FROM tickets
			WHERE date(fecha_creacion) is not null
			GROUP BY date(fecha_creacion);"""
	tickets_abiertos = db.engine.execute(query)
	tickets_abiertos = [{'fecha': tc[0], 'cantidad': tc[1]} for tc in tickets_abiertos]
	tickets_abiertos = completar_ceros(tickets_abiertos)

	return tickets_cerrados, tickets_abiertos

def obtener_data_acumulada():
	tickets_cerrados, tickets_abiertos = obtener_data_diaria()
	acumulado_tickets_creados = []
	acumulado = 0
	for ticket in tickets_abiertos:
		sumar = ticket["cantidad"]
		restar = 0
		for cerrado in tickets_cerrados:
			if cerrado["fecha"] == ticket["fecha"]:
				restar = cerrado["cantidad"]

		acumulado = acumulado + sumar - restar
		acumulado_tickets_creados.append({"fecha":ticket["fecha"],"cantidad":acumulado})

	return acumulado_tickets_creados