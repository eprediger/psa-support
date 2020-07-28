from main.db.database import (agregar_instancia, editar_instancia, eliminar_instancia,
                      obtener_instancias_por_filtro,
                      obtener_todas_las_instancias, obtener_una_instancia)
from main.models.Cliente import Cliente
from main.models.Ticket import Ticket

from datetime import datetime, timedelta
from pytz import timezone

def obtener_clientes():
	clientes = obtener_todas_las_instancias(Cliente)
	return [c.a_diccionario() for c in clientes]

def obtener_cliente_por(id):
	cliente = obtener_una_instancia(Cliente, id=id)
	return cliente.a_diccionario()

def crear(cliente):
	fecha_creacion = datetime.now(timezone('America/Argentina/Buenos_Aires'))

	c = agregar_instancia(Cliente,
						razon_social=cliente["razon_social"],
						descripcion=cliente["descripcion"],
						CUIT=cliente["CUIT"],
						fecha_desde_que_es_cliente=fecha_creacion)

	return c.a_diccionario()

def editar(id, cliente):
	editar_instancia(Cliente, id,
				razon_social=cliente["razon_social"],
				descripcion=cliente["descripcion"],
				CUIT=cliente["CUIT"],
				estado=cliente["estado"])

def eliminar(id):
	cliente = obtener_una_instancia(Cliente, id=id)

	if not cliente:
		raise Exception("No existe el cliente solicitado")

	ticket_asociado = obtener_una_instancia(Ticket, id_cliente=id)

	if ticket_asociado:
	 	raise Exception('No se puede eliminar el cliente solicitado ya que está asignado a un ticket')

	eliminar_instancia(Cliente, id=id)
