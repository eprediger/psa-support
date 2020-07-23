from flask_sqlalchemy import SQLAlchemy

from main.db.database import db, editar_instancia

class Cliente(db.Model):
    """
    Clase que define la tabla Cliente
    """

    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(150), nullable=False)
    CUIT = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.String(300), nullable=False)
    fecha_desde_que_es_cliente = db.Column(db.DateTime(timezone=True), nullable=True)
    estado = db.Column(db.Enum('activo', 'inactivo'), nullable=False,
                               default='activo')

    def a_diccionario(self):
        '''
        Retorna el diccionario de la instancia
        '''
        d = {
            'id': self.id,
            'razon_social': self.razon_social,
            'CUIT': self.CUIT,
            'descripcion': self.descripcion,
            'fecha_desde_que_es_cliente': self.fecha_desde_que_es_cliente.strftime('%d/%m/%Y'),
            'estado': self.estado
        }
        return d
