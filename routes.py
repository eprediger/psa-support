from flask import request, jsonify
from models import Ticket
from flask.blueprints import Blueprint
from settings import CODIGO_HTTP_BAD_REQUEST, CODIGO_HTTP_NOT_FOUND,\
					 CODIGO_HTTP_OK, SEVERIDADES
from database import obtener_una_instancia, agregar_instancia,\
                     editar_instancia, eliminar_instancia
from datetime import datetime, timedelta
from pytz import timezone


tickets = Blueprint('tickets', __name__)


@tickets.route('/tickets', methods=['GET'])
def obtener_tickets():
	tickets = Ticket.query.all()
	todos_los_tickets = [t.a_diccionario() for t in tickets]
	return jsonify({'tickets': todos_los_tickets}), CODIGO_HTTP_OK


@tickets.route('/tickets', methods=['POST'])
def crear_ticket():
	try:
		data = request.get_json()
		nombre = data['nombre']
		descripcion = data['descripcion']
		tipo = data['tipo'].lower()
		severidad = data['severidad'].lower()
#		pasos = data['pasos']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	if severidad not in SEVERIDADES.keys():
		return jsonify({'mensaje': 'La severidad debe ser Alta, Media o Baja'}), CODIGO_HTTP_BAD_REQUEST
	
	if tipo not in ['error', 'consulta', 'mejora']:
		return jsonify({'mensaje': 'El tipo de ticket debe ser Error/Consulta/Mejora'}), CODIGO_HTTP_BAD_REQUEST
	
	if tipo != 'error':
		pasos = None

	fecha_creacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))
	fecha_limite = fecha_creacion + timedelta(days=SEVERIDADES[severidad])

	t = agregar_instancia(Ticket, nombre=nombre, descripcion=descripcion,
						  tipo=tipo, severidad=severidad,
						  fecha_creacion=fecha_creacion, 
						  fecha_limite=fecha_limite,
						  fecha_ultima_actualizacion=fecha_creacion,
						  pasos=pasos)
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
		responsable = data['responsable']
		pasos = data['pasos']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	ticket = obtener_una_instancia(Ticket, id=id_ticket)
	
	if ticket.estado.lower() == 'cerrado':
		return jsonify({'mensaje': 'El ticket ya fue cerrado previamente'}), CODIGO_HTTP_BAD_REQUEST

	if not ticket:
		return jsonify({'mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND
	
	if severidad not in SEVERIDADES.keys():
		return jsonify({'mensaje': 'La severidad debe ser Alta, Media o Baja'}), CODIGO_HTTP_BAD_REQUEST
	
	if tipo not in ['error', 'consulta', 'mejora']:
		return jsonify({'mensaje': 'El tipo de ticket debe ser Error/Consulta/Mejora'}), CODIGO_HTTP_BAD_REQUEST

	if estado not in ['nuevo', 'asignado', 'cerrado']:
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
						  responsable=responsable,
						  pasos=pasos)

	return jsonify({'mensaje': 'Ticket actualizado con exito!'}), CODIGO_HTTP_OK


@tickets.route('/tickets/<int:id_ticket>', methods=['DELETE'])
def archivar_ticket(id_ticket):
	ticket = obtener_una_instancia(Ticket, id=id_ticket)
	
	if not ticket:
		return jsonify({'mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND

	eliminar_instancia(Ticket, id=id_ticket)
	return jsonify({'mensaje': 'Ticket eliminado con exito!'}), CODIGO_HTTP_OK