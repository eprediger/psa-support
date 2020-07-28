from flask_sqlalchemy import SQLAlchemy

from main.db.database import db, editar_instancia


class TicketTarea(db.Model):
    """
    Clase que define la tabla Ticket
    """

    __tablename__ = 'tickets_tareas'

    # Foreigns and relations
    id_ticket = db.Column(db.Integer(), 
                          db.ForeignKey('tickets.id'),
                          primary_key=True,
                          nullable=False)
    tickets = db.relationship('Ticket', backref='tareas')
    id_proyecto = db.Column(db.Integer())
    id_tarea = db.Column(db.Integer(), primary_key=True)

    def a_diccionario(self):
        ''' Retorna el diccionario de la instancia
        '''
        d = {
            'id_ticket': self.id_ticket,
            'id_tarea': self.id_tarea,
            'id_proyecto': self.id_proyecto
        }
        return d
