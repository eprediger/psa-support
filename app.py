from decouple import config as config_decouple
from flask import Flask
from flask_cors import CORS

from config import config
from database import db
from routes import clientes, tickets

from flask_swagger_ui import get_swaggerui_blueprint


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PSA-SOPORTE"
    }
)
### end swagger specific ###


def create_app(env):
    app = Flask(__name__)
    cors = CORS(app)

    app.config.from_object(env)

    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    app.register_blueprint(tickets)
    app.register_blueprint(clientes)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app

environment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app = create_app(environment)

if __name__ == '__main__':
    app.run()
