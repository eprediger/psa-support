
from flask import jsonify, request
from flask.blueprints import Blueprint

from main.service.clientes_service import (obtener_clientes as obtener_clientes_service,
                                           crear, editar, obtener_cliente_por, eliminar)
from main.settings import (CODIGO_HTTP)

clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes', methods=['GET'])
def obtener_clientes():
	respuesta = obtener_clientes_service()
	return jsonify(respuesta), CODIGO_HTTP["OK"]

@clientes.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
	try:
		cliente = obtener_cliente_por(id)
		return jsonify(cliente), CODIGO_HTTP["OK"]
	except:
		return jsonify({'mensaje': 'Cliente no encontrado'}), CODIGO_HTTP["BAD_REQUEST"]

@clientes.route('/clientes', methods=['POST'])
def crear_cliente():
	try:
		data = request.get_json()
		for d in data:
			if data[d] == None:
				return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP["BAD_REQUEST"]

		cliente = crear(data)

		return jsonify(cliente), CODIGO_HTTP["CREATED"]
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP["BAD_REQUEST"]

@clientes.route('/clientes/<int:id>', methods=['PUT'])
def editar_cliente(id):
	try:
		data = request.get_json()
		for d in data:
			if data[d] == None:
				return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP["BAD_REQUEST"]

		editar(id, data)

		return jsonify(), CODIGO_HTTP["NO_CONTENT"]
	except:
		return jsonify({'mensaje': 'Parametros invalidos'}), CODIGO_HTTP["BAD_REQUEST"]

@clientes.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def eliminar_cliente(id_cliente):
	try:
		eliminar(id_cliente)
		return jsonify({'mensaje': 'Cliente eliminado con exito!'}), CODIGO_HTTP["OK"]
	except Exception as e:
		return jsonify({'mensaje': str(e)}), CODIGO_HTTP["NOT_FOUND"]
