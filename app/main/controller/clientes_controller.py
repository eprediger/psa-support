from datetime import datetime, timedelta

from flask import jsonify, request
from flask.blueprints import Blueprint
from pytz import timezone

from database import (agregar_instancia, editar_instancia, eliminar_instancia,
                      obtener_instancias_por_filtro,
                      obtener_todas_las_instancias, obtener_una_instancia)
from models import Cliente
from settings import (CODIGO_HTTP_BAD_REQUEST, CODIGO_HTTP_NO_CONTENT,
                      CODIGO_HTTP_NOT_FOUND, CODIGO_HTTP_OK, SEVERIDADES)

clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes', methods=['GET'])
def obtener_clientes():
	clientes = obtener_todas_las_instancias(Cliente)
	todos_los_clientes = [c.a_diccionario() for c in clientes]
	return jsonify(todos_los_clientes), CODIGO_HTTP_OK

@clientes.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
	try:
		cliente = obtener_una_instancia(Cliente, id=id)
		return jsonify(cliente.a_diccionario()), CODIGO_HTTP_OK
	except:
		return jsonify({'mensaje': 'Cliente no encontrado'}), CODIGO_HTTP_BAD_REQUEST

@clientes.route('/clientes', methods=['POST'])
def crear_cliente():
	try:
		data = request.get_json()
		razon_social = data['razon_social']
		descripcion = data['descripcion']
		CUIT = data['CUIT']
		#fecha_desde_que_es_cliente = data['fecha_desde_que_es_cliente']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	for d in data:
		if data[d] == None:
			return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	fecha_creacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))

	c = agregar_instancia(Cliente,
						razon_social=razon_social,
						descripcion=descripcion,
						CUIT=CUIT,
						fecha_desde_que_es_cliente=fecha_creacion)
	cliente_diccionario = c.a_diccionario()

	return jsonify(cliente_diccionario), CODIGO_HTTP_OK

@clientes.route('/clientes/<int:id>', methods=['PUT'])
def editar_cliente(id):
	try:
		data = request.get_json()
		razon_social = data['razon_social']
		descripcion = data['descripcion']
		CUIT = data['CUIT']
		estado = data['estado']
		#fecha_desde_que_es_cliente = data['fecha_desde_que_es_cliente']
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	for d in data:
		if data[d] == None:
			return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP_BAD_REQUEST

	editar_instancia(Cliente, id, razon_social=razon_social,
					descripcion=descripcion,
					CUIT=CUIT,
					estado=estado
					#fecha_desde_que_es_cliente=fecha_desde_que_es_cliente
					)

	return jsonify(), CODIGO_HTTP_NO_CONTENT

@clientes.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def eliminar_cliente(id_cliente):
	cliente = obtener_una_instancia(Cliente, id=id_cliente)

	if not cliente:
		return jsonify({'mensaje': 'No existe el cliente solicitado'}), CODIGO_HTTP_NOT_FOUND

	ticket_asociado = obtener_una_instancia(Ticket, id_cliente=id_cliente)

	if ticket_asociado:
	 	return jsonify({'mensaje': 'No se puede eliminar el cliente solicitado ya que está asignado a un ticket'}), CODIGO_HTTP_BAD_REQUEST

	eliminar_instancia(Cliente, id=id_cliente)
	return jsonify({'mensaje': 'Cliente eliminado con exito!'}), CODIGO_HTTP_OK
