from flask import request, jsonify
from models import Ticket, Cliente
from flask.blueprints import Blueprint
from settings import CODIGO_HTTP_BAD_REQUEST, CODIGO_HTTP_NOT_FOUND,\
					 CODIGO_HTTP_OK, SEVERIDADES
from database import obtener_una_instancia, agregar_instancia,\
                     editar_instancia, eliminar_instancia
from datetime import datetime, timedelta
from pytz import timezone


tickets = Blueprint('tickets', __name__)
clientes = Blueprint('clientes', __name__)


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
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST
	
	try:
		pasos = data['pasos']
	except:
		pasos = None

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
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST
	
	try:
		id_cliente = data['id_cliente']
	except:
		id_cliente = None

	try:
		pasos = data['pasos']
	except:
		pasos = None

	ticket = obtener_una_instancia(Ticket, id=id_ticket)
	
	if not ticket:
		return jsonify({'Mensaje': 'No existe el ticket solicitado'}), 404

	if ticket.estado:
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
						pasos=pasos,
						id_cliente=id_cliente)	

	return jsonify({'mensaje': 'Ticket actualizado con exito!'}), CODIGO_HTTP_OK

@tickets.route('/tickets/<int:id_ticket>', methods=['DELETE'])
def archivar_ticket(id_ticket):
	ticket = obtener_una_instancia(Ticket, id=id_ticket)
	
	if not ticket:
		return jsonify({'mensaje': 'No existe el ticket solicitado'}), CODIGO_HTTP_NOT_FOUND

	if ticket.estado.lower() != 'cerrado':
		return jsonify({'mensaje': 'Los tickets deben estar cerrados para poder archivarse!'}), CODIGO_HTTP_BAD_REQUEST

	eliminar_instancia(Ticket, id=id_ticket)
	return jsonify({'mensaje': 'Ticket archivado con exito!'}), CODIGO_HTTP_OK

@clientes.route('/clientes', methods=['GET'])
def obtener_clientes():
	clientes = Cliente.query.all()
	todos_los_clientes = [c.a_diccionario() for c in clientes]
	return jsonify({'clientes': todos_los_clientes}), CODIGO_HTTP_OK


@clientes.route('/clientes', methods=['POST'])
def crear_cliente():
	try:
		data = request.get_json()
		razon_social = data['razon_social']
		descripcion = data['descripcion']
		CUIT = data['CUIT']
		fecha_desde_que_es_cliente = data['fecha_desde_que_es_cliente']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	for d in data:
		if data[d] == None:
			return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	c = agregar_instancia(Cliente, 
						razon_social=razon_social, 
						descripcion=descripcion,
						CUIT=CUIT,
						fecha_desde_que_es_cliente=fecha_desde_que_es_cliente)
	cliente_diccionario = c.a_diccionario()

	return jsonify(cliente_diccionario), CODIGO_HTTP_OK

@tickets.route('/clientes/<int:id>', methods=['PUT'])
def editar_cliente(id):
	try:
		data = request.get_json()
		razon_social = data['razon_social']
		descripcion = data['descripcion']
		CUIT = data['CUIT']
		fecha_desde_que_es_cliente = data['fecha_desde_que_es_cliente']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	for d in data:
		if data[d] == None:
			return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	editar_instancia(Cliente, id, razon_social=razon_social,
					descripcion=descripcion,
					CUIT=CUIT,
					fecha_desde_que_es_cliente=fecha_desde_que_es_cliente
					)	

	return jsonify({'mensaje': 'Ticket actualizado con exito!'}), CODIGO_HTTP_OK

@clientes.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def eliminar_cliente(id_cliente):
	cliente = obtener_una_instancia(Cliente, id=id_cliente)
	
	if not cliente:
		return jsonify({'mensaje': 'No existe el cliente solicitado'}), CODIGO_HTTP_NOT_FOUND

	if cliente.asignado:
	 	return jsonify({'mensaje': 'No se puede eliminar el cliente solicitado ya que está asignado a un ticket'}), CODIGO_HTTP_BAD_REQUEST

	eliminar_instancia(Cliente, id=id_cliente)
	return jsonify({'mensaje': 'Cliente eliminado con exito!'}), CODIGO_HTTP_OK