from flask import request, jsonify
from models import Ticket
from flask.blueprints import Blueprint
from settings import CODIGO_HTTP_BAD_REQUEST, CODIGO_HTTP_NOT_FOUND,\
					 CODIGO_HTTP_OK
from database import obtener_una_instancia, agregar_instancia,\
                     editar_instancia, eliminar_instancia


tickets = Blueprint('tickets', __name__)


@tickets.route('/')
def hello():
	return "Hello World!"


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
		tipo = data['tipo']
		estado = data['estado']
		severidad = data['severidad']
		fecha_creacion = data['fecha_creacion']
		fecha_ultima_actualizacion = data['fecha_ultima_actualizacion']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	t = agregar_instancia(Ticket, nombre=nombre, descripcion=descripcion,
						  tipo=tipo, estado=estado, severidad=severidad,
						  fecha_creacion=fecha_creacion,
						  fecha_ultima_actualizacion=fecha_ultima_actualizacion)
	ticket_diccionario = t.a_diccionario()

	return jsonify(ticket_diccionario), CODIGO_HTTP_OK


@tickets.route('/tickets/<int:id_ticket>', methods=['PUT'])
def editar_ticket(id_ticket):
	
	try:
		data = request.get_json()
		nombre = data['nombre']
		descripcion = data['descripcion']
		tipo = data['tipo']
		estado = data['estado']
		severidad = data['severidad']
		fecha_creacion = data['fecha_creacion']
		fecha_ultima_actualizacion = data['fecha_ultima_actualizacion']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST


	ticket = obtener_una_instancia(Ticket, id=id_ticket)
	
	if not ticket:
		return jsonify({'mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND
	
	editar_instancia(Ticket, id_ticket, nombre=nombre, descripcion=descripcion,
						  tipo=tipo, estado=estado, severidad=severidad,
						  fecha_creacion=fecha_creacion,
						  fecha_ultima_actualizacion=fecha_ultima_actualizacion)

	return jsonify({'mensaje': 'Ticket actualizado con exito!'}), CODIGO_HTTP_OK


@tickets.route('/tickets/<int:id_ticket>', methods=['DELETE'])
def eliminar_ticket(id_ticket):
	ticket = obtener_una_instancia(Ticket, id=id_ticket)
	
	if not ticket:
		return jsonify({'mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND
	
	eliminar_instancia(Ticket, id=id_ticket)

	return jsonify({'mensaje': 'Ticket eliminado con exito!'}), CODIGO_HTTP_OK