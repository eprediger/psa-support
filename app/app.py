from main.config import config
from main.controller.clientes_controller import clientes
from main.controller.tickets_controller import tickets
from main.db.database import db
from main.settings import SWAGGER_URL, SWAGGERUI_BLUEPRINT

from decouple import config as config_decouple
from flask import Flask
from flask_cors import CORS


def create_app(env):
    app = Flask(__name__)
    cors = CORS(app)

    app.config.from_object(env)

    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    app.register_blueprint(tickets)
    app.register_blueprint(clientes)

    with app.app_context():
#        db.init_app(app)
        """
        TEORIA:
        - Heroku apaga el proceso por inactividad.
         Al invocar un servicio, se ejecuta este método, crea tablas que ya existen y pincha.

        Si se borra la base:
        heroku run python
        > from main.db.database import db
        > db.create_all()
        """
        if not db.engine.has_table('clientes'):
            
            print("HOlis")
#            db.create_all()

    return app

environment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app = create_app(environment)

if __name__ == '__main__':
    app.run()
