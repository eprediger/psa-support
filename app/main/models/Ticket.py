from flask_sqlalchemy import SQLAlchemy

from main.db.database import db, editar_instancia


class Ticket(db.Model):
    """
    Clase que define la tabla Ticket
    """

    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=True)
    descripcion = db.Column(db.String(300), nullable=True)
    tipo = db.Column(db.Enum('error', 'consulta', 'mejora'),
                     nullable=False)
    estado = db.Column(db.Enum('nuevo', 'en progreso', 'esperando informacion',
                               'cerrado'), nullable=False,
                               default='nuevo')
    severidad = db.Column(db.Enum('baja', 'media', 'alta'),
                          nullable=True)
    legajo_responsable = db.Column(db.Integer, nullable=True)
    pasos = db.Column(db.String(300), nullable=True, default='')
    fecha_creacion = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_limite = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_finalizacion = db.Column(db.DateTime(timezone=True), nullable=True)
    fecha_ultima_actualizacion = db.Column(db.DateTime(timezone=True), nullable=True)

    # Foreigns and relations
    id_cliente = db.Column(db.Integer(),
                           db.ForeignKey('clientes.id'),
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

        if self.cliente:
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
            'legajo_responsable': self.legajo_responsable,
            'fecha_creacion': fecha_creacion,
            'fecha_limite': fecha_limite,
            'fecha_finalizacion': fecha_finalizacion,
            'fecha_ultima_actualizacion': fecha_actualizacion,
            'cliente' : cliente
        }
        return d
