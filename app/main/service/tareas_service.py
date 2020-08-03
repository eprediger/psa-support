from main.models.TicketTarea import TicketTarea
from main.service.tickets_service import obtener_ticket_por
from main.db.database import agregar_instancia

def crear_tarea(tarea, id_ticket):
	ticket = obtener_ticket_por(id=id_ticket)
	if not ticket:
		raise Exception('No existe el ticket solicitado')

	id_tarea = tarea['id_tarea']
	id_proyecto = tarea['id_proyecto']

	agregar_instancia(TicketTarea,
					id_ticket=id_ticket,
					id_tarea=id_tarea,
					id_proyecto=id_proyecto)
