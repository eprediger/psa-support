from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


def agregar_instancia(model, **kwargs):
    """Agrega una instancia con todos sus pares key=value de atributos
    """
    instance = model(**kwargs)
    db.session.add(instance)
    commitear_cambios()
    return instance


def eliminar_instancia(model, id):
    """Elimina una instancia por id
    """
    m = model.query.filter_by(id=id).first()
    db.session.delete(m)
    commitear_cambios()


def eliminar_instancias_filtradas(model, **kwargs):
    """Elimina varias instancias por filtro
    """
    instancias = model.query.filter_by(**kwargs)#.delete()
    for i in instancias:
        db.session.delete(i)
    commitear_cambios()


def editar_instancia(model, id, **kwargs):
    """Edita los pares key=value de atributos recibidos de una instancia.
    Si el value es None no actualiza.
    """
    instance = model.query.filter_by(id=id).all()[0]

    for attr, new_value in kwargs.items():
        if ((type(new_value) == bool) or new_value is None):
            setattr(instance, attr, new_value)
        else:
            if new_value:
                setattr(instance, attr, new_value)
    agregar_y_commitear(instance)


def commitear_cambios():
    """Commitea los cambios
    """
    db.session.commit()


def agregar_y_commitear(*args):
    """Recibe muchas instancias, la agregas a la base y commitea
    """
    for arg in args:
        db.session.add(arg)

    commitear_cambios()

def obtener_todas_las_instancias(model, ordenClave=None):
    if ordenClave:
        instancias = model.query.order_by(text(f"{ordenClave} desc")).all()
    else:
        instancias = model.query.all()
    return instancias

def obtener_una_instancia(model, **kwargs):
    """Devuelve la primer instancia filtrada segun la llave/valor
    del argumento
    """
    instancia = model.query.filter_by(**kwargs).first()
    return instancia

def obtener_instancias_por_filtro(model, **kwargs):
	"""
	Devuelve las instancias que cumplan con los filtros
	"""

	instancias = model.query.filter_by(**kwargs)
	return instancias
