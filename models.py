from flask_sqlalchemy import SQLAlchemy
from database import db


class Ticket(db.Model):
    """Clase que define la tabla Ticket
    """
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=True)
    descripcion = db.Column(db.String(150), nullable=True)
    tipo = db.Column(db.String(150), nullable=True)
    estado = db.Column(db.Enum('Nuevo', 'Asignado',
                               'Cerrado'), nullable=True)
    severidad = db.Column(db.String(150), nullable=True)
    fecha_creacion = db.Column(db.String(150), nullable=False)
    fecha_ultima_actualizacion = db.Column(db.String(150), nullable=False)

    def a_diccionario(self):
        ''' Retorna el diccionario de la instancia 
        '''
        d = {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'estado': self.estado,
            'severidad': self.severidad,
            'fecha_limite': self.fecha_creacion,
            'fecha_ultima_actualizacion': self.fecha_ultima_actualizacion
        }
        return d
