from flask import jsonify, request
from flask.blueprints import Blueprint

from main.service.tareas_service import crear_tarea
from main.service.tickets_service import (archivar, crear, editar,
                                          obtener_ticket_por, obtener_data_diaria, obtener_data_acumulada, crear_data_relleno)
from main.service.tickets_service import \
    obtener_tickets as obtener_tickets_service
from main.settings import CODIGO_HTTP

tickets = Blueprint('tickets', __name__)


@tickets.route('/tickets', methods=['GET'])
def obtener_tickets():
	query_params = request.args

	respuesta = obtener_tickets_service(query_params)

	return jsonify(respuesta), CODIGO_HTTP["OK"]

@tickets.route('/tickets/<int:id>', methods=['GET'])
def obtener_ticket(id):
	try:
		ticket = obtener_ticket_por(id)
		return jsonify(ticket), CODIGO_HTTP["OK"]
	except:
		return jsonify({'mensaje': 'Ticket no encontrado'}), CODIGO_HTTP["BAD_REQUEST"]

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
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP["BAD_REQUEST"]
	
	try:
		ticket = crear(data)

		return jsonify(ticket), CODIGO_HTTP["OK"]
	except Exception as e:
		return jsonify({'mensaje': str(e)}), CODIGO_HTTP["BAD_REQUEST"]

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
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP["BAD_REQUEST"]

	try:
		editar(id_ticket, data)

		return jsonify(), CODIGO_HTTP["NO_CONTENT"]
	except Exception as e:
		return jsonify({'mensaje': str(e)}), CODIGO_HTTP["BAD_REQUEST"]


@tickets.route('/tickets/<int:id_ticket>', methods=['DELETE'])
def archivar_ticket(id_ticket):
	try:
		archivar(id_ticket)
		return jsonify({'mensaje': 'Ticket archivado con exito!'}), CODIGO_HTTP["OK"]
	except Exception as e:
		return jsonify({'mensaje': str(e)}), CODIGO_HTTP["BAD_REQUEST"]

@tickets.route('/tickets/<int:id_ticket>/tareas', methods=['POST'])
def crear_tarea_derivada(id_ticket):
	try:
		data = request.get_json()

		crear_tarea(data, id_ticket)
		# ('No existe el ticket solicitado'), CODIGO_HTTP["NOT_FOUND"]

		return jsonify({'mensaje': "Tarea asociada a ticket exitosamente"}), CODIGO_HTTP["OK"]
	except Exception as e:
		return jsonify({'mensaje': str(e)}), CODIGO_HTTP["BAD_REQUEST"]

@tickets.route('/tickets/data_diaria', methods=['GET'])
def data_diaria():
	tickets_cerrados, tickets_abiertos = obtener_data_diaria()
	return {'tickets_cerrados' : tickets_cerrados, 'tickets_abiertos' : tickets_abiertos}



@tickets.route('/tickets/data_acumulada', methods=['GET'])
def data_acumulada():
	return jsonify(obtener_data_acumulada())