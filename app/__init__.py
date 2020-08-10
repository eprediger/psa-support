from app.main.config import config
from app.main.controller.clientes_controller import clientes
from app.main.controller.tickets_controller import tickets
from app.main.db.database import db
from app.main.settings import SWAGGER_URL, SWAGGERUI_BLUEPRINT

from decouple import config as config_decouple
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists


def create_app(env):
    app = Flask(__name__)
    cors = CORS(app)

    app.config.from_object(env)

    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    app.register_blueprint(tickets)
    app.register_blueprint(clientes)

    db.init_app(app)
    Migrate(app, db)

    return app

environment = config['production']
if config_decouple('PRODUCTION', default=False):
    print("LALAL produccion")
    environment = config['production']
    print("La variable de la base eeess:::")
    print(environment.SQLALCHEMY_DATABASE_URI)
    print("")
else:
    print("la connn!!")

app = create_app(environment)

if __name__ == '__main__':
    app.run()
