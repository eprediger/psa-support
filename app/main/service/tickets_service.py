from datetime import datetime, timedelta

from pytz import timezone

from main.db.database import (agregar_instancia, editar_instancia,
                              eliminar_instancia,
                              obtener_instancias_por_filtro,
                              obtener_todas_las_instancias,
                              obtener_una_instancia)
from main.models.Ticket import Ticket
from main.settings import SEVERIDADES


def obtener_tickets(query_params):
	tickets = []

	if query_params:
		tickets = obtener_instancias_por_filtro(Ticket, **query_params)
	else:
		tickets = obtener_todas_las_instancias(Ticket)

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
	ticket_almacenado = obtener_ticket_por(id)

	if not ticket_almacenado:
		raise Exception("No existe el ticket solicitado")

	id_cliente = ticket_editado["cliente"]["id"]
	pasos = ticket_editado.get('pasos')
	responsable = ticket_editado.get('legajo_responsable')

	estado = ticket_editado['estado'].lower()

	if ticket_editado["estado"] and ticket_editado["estado"].lower() == 'cerrado':
		raise Exception('El ticket ya fue cerrado previamente')

	if estado not in ['nuevo', 'en progreso', 'cerrado', 'esperando informacion']:
		raise Exception('El estado de ticket debe ser Nuevo/Asignado/Cerrado')
	# , CODIGO_HTTP["BAD_REQUEST"]

	fecha_ultima_actualizacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))
	if estado == 'cerrado' and ticket_almacenado["estado"] != 'cerrado':
		# Si cambio al estado cerrado, se coloca la fecha de finalización.
		fecha_finalizacion = fecha_ultima_actualizacion
	else:
		fecha_finalizacion = None

	severidad = ticket_editado['severidad'].lower()
	if severidad not in SEVERIDADES.keys():
		raise Exception('La severidad debe ser Alta, Media o Baja')

	if severidad != ticket["severidad"]:
		# Si cambiaron la severidad del ticket, se actualiza la fecha limite.
		fecha_limite = ticket["fecha_creacion"] + timedelta(days=SEVERIDADES[severidad.lower()])
	else:
		fecha_limite = ticket["fecha_limite"]

	tipo = ticket_editado['tipo'].lower()

	if tipo not in ['error', 'consulta', 'mejora']:
		raise Exception('El tipo de ticket debe ser Error/Consulta/Mejora')
	# , CODIGO_HTTP["BAD_REQUEST"]

	if tipo != 'error':
		# Solo los tickets de tipo error llevan pasos
		pasos = None

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
						id_cliente=id_cliente)

def archivar(id):
	ticket = obtener_una_instancia(Ticket, id=id)

	if not ticket:
		raise Exception('No existe el ticket solicitado')
	# , CODIGO_HTTP["NOT_FOUND"]

	if ticket.estado.lower() != 'cerrado':
		raise Exception('Los tickets deben estar cerrados para poder archivarse!')
	# , CODIGO_HTTP["BAD_REQUEST"]

	eliminar_instancia(Ticket, id=id)
