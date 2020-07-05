from flask import Flask
from routes import tickets, clientes
from database import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def create_app(dev=True):
	app.config['DEBUG'] = dev
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	db.init_app(app)
	app.register_blueprint(tickets)
	app.register_blueprint(clientes)
	return app

def setup_database(app):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_app()
    setup_database(app)
    app.run()
