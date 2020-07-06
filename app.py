from decouple import config as config_decouple
from flask import Flask

from config import config
from database import db
from flask_cors import CORS
from routes import clientes, tickets

def create_app(env):
    app = Flask(__name__)
    CORS(app, resources={r'/*': {"origins": "*"}})

    app.config.from_object(env)

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
