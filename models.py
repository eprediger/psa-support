from flask_sqlalchemy import SQLAlchemy
from database import db


class Ticket(db.Model):
    """Clase que define la tabla Ticket
    """
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=True)
    descripcion = db.Column(db.String(150), nullable=True)
    tipo = db.Column(db.Enum('error', 'consulta', 'mejora'),
                     nullable=False)
    estado = db.Column(db.Enum('nuevo', 'asignado',
                               'cerrado'), nullable=False,
                               default='nuevo')
    severidad = db.Column(db.Enum('baja', 'media', 'alta'),
                          nullable=True)
    responsable = db.Column(db.String(40), nullable=True)
    fecha_creacion = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_limite = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_finalizacion = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_ultima_actualizacion = db.Column(db.DateTime(timezone=True), nullable=True)

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
            'responsable': self.responsable,
            'fecha_creacion': self.fecha_creacion,
            'fecha_limite': self.fecha_limite,
            'fecha_finalizacion': self.fecha_finalizacion,
            'fecha_ultima_actualizacion': self.fecha_ultima_actualizacion
        }
        return d
