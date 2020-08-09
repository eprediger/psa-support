from app.app import create_app
from decouple import config as config_decouple
from main.config import config

environment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']
app = create_app()