from datetime import datetime, timedelta

from flask import jsonify, request
from flask.blueprints import Blueprint
from pytz import timezone

from main.db.database import (agregar_instancia, editar_instancia, eliminar_instancia,
                      obtener_instancias_por_filtro,
                      obtener_todas_las_instancias, obtener_una_instancia)
from main.models.Ticket import Ticket
from main.models.TicketTarea import TicketTarea
from main.settings import (CODIGO_HTTP_BAD_REQUEST, CODIGO_HTTP_NO_CONTENT,
                      CODIGO_HTTP_NOT_FOUND, CODIGO_HTTP_OK, SEVERIDADES)


tickets = Blueprint('tickets', __name__)

@tickets.route('/tickets', methods=['GET'])
def obtener_tickets():
	tickets = []

	query_params = request.args
	if query_params:
		tickets = obtener_instancias_por_filtro(Ticket, **query_params)
	else:
		tickets = obtener_todas_las_instancias(Ticket)

	respuesta = [t.a_diccionario() for t in tickets]

	return jsonify(respuesta), CODIGO_HTTP_OK

@tickets.route('/tickets/<int:id>', methods=['GET'])
def obtener_ticket(id):
	try:
		ticket = obtener_una_instancia(Ticket, id=id)
		return jsonify(ticket.a_diccionario()), CODIGO_HTTP_OK
	except:
		return jsonify({'mensaje': 'Ticket no encontrado'}), CODIGO_HTTP_BAD_REQUEST


@tickets.route('/tickets', methods=['POST'])
def crear_ticket():
	try:
		data = request.get_json()
		nombre = data['nombre']
		descripcion = data['descripcion']
		tipo = data['tipo'].lower()
		severidad = data['severidad'].lower()
		id_cliente = data['cliente']['id']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	try:
		pasos = data['pasos']
	except:
		pasos = None

	try:
		legajo_responsable = data['legajo_responsable']
	except:
		legajo_responsable = None

	if severidad not in SEVERIDADES.keys():
		return jsonify({'mensaje': 'La severidad debe ser Alta, Media o Baja'}), CODIGO_HTTP_BAD_REQUEST

	if tipo not in ['error', 'consulta', 'mejora']:
		return jsonify({'mensaje': 'El tipo de ticket debe ser Error/Consulta/Mejora'}), CODIGO_HTTP_BAD_REQUEST

	fecha_creacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))
	fecha_limite = fecha_creacion + timedelta(days=SEVERIDADES[severidad])

	t = agregar_instancia(Ticket, nombre=nombre, descripcion=descripcion,
						  tipo=tipo, severidad=severidad,
						  fecha_creacion=fecha_creacion,
						  fecha_limite=fecha_limite,
						  fecha_ultima_actualizacion=fecha_creacion,
						  pasos=pasos,
						  id_cliente=id_cliente,
						  legajo_responsable=legajo_responsable)

	ticket_diccionario = t.a_diccionario()

	return jsonify(ticket_diccionario), CODIGO_HTTP_OK


@tickets.route('/tickets/<int:id_ticket>', methods=['PUT'])
def editar_ticket(id_ticket):
	try:
		data = request.get_json()
		nombre = data['nombre']
		descripcion = data['descripcion']
		tipo = data['tipo'].lower()
		estado = data['estado'].lower()
		severidad = data['severidad'].lower()
		id_cliente = data['cliente']['id']
	except:
		print('\n \n \n \n \n \n \n \n\n \n \n SISI')
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	try:
		pasos = data['pasos']
	except:
		pasos = None

	try:
		responsable = data['legajo_responsable']
	except:
		responsable = None

	ticket = obtener_una_instancia(Ticket, id=id_ticket)

	if not ticket:
		return jsonify({'Mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND

	if ticket.estado:
		if ticket.estado.lower() == 'cerrado':
			return jsonify({'mensaje': 'El ticket ya fue cerrado previamente'}), CODIGO_HTTP_BAD_REQUEST

	if severidad not in SEVERIDADES.keys():
		return jsonify({'mensaje': 'La severidad debe ser Alta, Media o Baja'}), CODIGO_HTTP_BAD_REQUEST

	if tipo not in ['error', 'consulta', 'mejora']:
		return jsonify({'mensaje': 'El tipo de ticket debe ser Error/Consulta/Mejora'}), CODIGO_HTTP_BAD_REQUEST

	if estado not in ['nuevo', 'en progreso', 'cerrado', 'esperando informaicon']:
		return jsonify({'mensaje': 'El estado de ticket debe ser Nuevo/Asignado/Cerrado'}), CODIGO_HTTP_BAD_REQUEST

	fecha_ultima_actualizacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))

	if severidad != ticket.severidad:
		# Si cambiaron la severidad del ticket, se actualiza la fecha limite.
		print('modificando fecha limite')
		fecha_limite = ticket.fecha_creacion + timedelta(days=SEVERIDADES[severidad.lower()])
	else:
		fecha_limite = ticket.fecha_limite

	if estado == 'cerrado' and ticket.estado != 'cerrado':
		# Si cambio al estado cerrado, se coloca la fecha de finalización.
		fecha_finalizacion = fecha_ultima_actualizacion
	else:
		fecha_finalizacion = None

	if tipo != 'error':
		# Solo los tickets de tipo error llevan pasos
		pasos = None

	editar_instancia(Ticket, id_ticket, nombre=nombre, descripcion=descripcion,
						tipo=tipo, estado=estado, severidad=severidad,
						fecha_ultima_actualizacion=fecha_ultima_actualizacion,
						fecha_limite=fecha_limite,
						fecha_finalizacion=fecha_finalizacion,
						legajo_responsable=responsable,
						pasos=pasos,
						id_cliente=id_cliente)

	return jsonify(), CODIGO_HTTP_NO_CONTENT

@tickets.route('/tickets/<int:id_ticket>', methods=['DELETE'])
def archivar_ticket(id_ticket):
	ticket = obtener_una_instancia(Ticket, id=id_ticket)

	if not ticket:
		return jsonify({'mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND

	if ticket.estado.lower() != 'cerrado':
		return jsonify({'mensaje': 'Los tickets deben estar cerrados para poder archivarse!'}), CODIGO_HTTP_BAD_REQUEST

	eliminar_instancia(Ticket, id=id_ticket)
	return jsonify({'mensaje': 'Ticket archivado con exito!'}), CODIGO_HTTP_OK


@tickets.route('/tickets/<int:id_ticket>/tareas', methods=['POST'])
def crear_tarea_derivada(id_ticket):
	ticket = obtener_una_instancia(Ticket, id=id_ticket)

	if not ticket:
		return jsonify({'mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND
	
	try:
		data = request.get_json()
		id_tarea = data['id_tarea']
		id_proyecto = data['id_proyecto']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST
	
	agregar_instancia(TicketTarea, id_ticket=id_ticket, id_tarea=id_tarea, id_proyecto=id_proyecto)

	return jsonify({'mensaje': "Tarea asociada a ticket exitosamente"}), CODIGO_HTTP_OK