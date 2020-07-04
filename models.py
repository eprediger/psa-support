from flask_sqlalchemy import SQLAlchemy
from database import db


class Ticket(db.Model):
    """Clase que define la tabla Ticket
    """
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=True)
    descripcion = db.Column(db.String(300), nullable=True)
    tipo = db.Column(db.Enum('error', 'consulta', 'mejora'),
                     nullable=False)
    estado = db.Column(db.Enum('nuevo', 'asignado',
                               'cerrado'), nullable=False,
                               default='nuevo')
    severidad = db.Column(db.Enum('baja', 'media', 'alta'),
                          nullable=True)
    responsable = db.Column(db.String(40), nullable=True)
    pasos = db.Column(db.String(300), nullable=True)
    fecha_creacion = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_limite = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_finalizacion = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_ultima_actualizacion = db.Column(db.DateTime(timezone=True), nullable=True)
    
    # Foreigns and relations
    id_cliente = db.Column(db.Integer(),
                           db.ForeignKey('cliente.id'),
                           nullable=True)
    cliente = db.relationship('Cliente', backref='cliente')

    def a_diccionario(self):
        ''' Retorna el diccionario de la instancia 
        '''
        if self.fecha_limite:
            fecha_limite = self.fecha_limite.strftime('%Y-%m-%d %H:%M:%S')
        else:
            fecha_limite = None
        if self.fecha_creacion:
            fecha_creacion = self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
        else:
            fecha_creacion = None
        if self.fecha_finalizacion:
            fecha_finalizacion = self.fecha_finalizacion.strftime('%Y-%m-%d %H:%M:%S')
        else:
            fecha_finalizacion = None
        if self.fecha_ultima_actualizacion:
            fecha_actualizacion = self.fecha_ultima_actualizacion.strftime('%Y-%m-%d %H:%M:%S')
        else:
            fecha_actualizacion = None
        if self.id_cliente:
            cliente = self.cliente.a_diccionario()
        else:
            cliente = None

        d = {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'estado': self.estado,
            'severidad': self.severidad,
            'pasos': self.pasos,
            'responsable': self.responsable,
            'fecha_creacion': fecha_creacion,
            'fecha_limite': fecha_limite,
            'fecha_finalizacion': fecha_finalizacion,
            'fecha_ultima_actualizacion': fecha_actualizacion,
            'cliente' : cliente
        }
        return d

class Cliente(db.Model):
    """Clase que define la tabla Cliente
    """
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(150), nullable=False)
    CUIT = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
#    fecha_desde_que_es_cliente = db.Column(db.DateTime(timezone=True), nullable=False)
    fecha_desde_que_es_cliente = db.Column(db.String(300), nullable=False)

    def a_diccionario(self):
        ''' Retorna el diccionario de la instancia 
        '''
        d = {
            'id': self.id,
            'razon_social': self.razon_social,
            'CUIT': self.CUIT,
            'descripcion': self.descripcion,
            'fecha_desde_que_es_cliente': self.fecha_desde_que_es_cliente
        }
        return d