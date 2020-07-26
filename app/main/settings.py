from flask_swagger_ui import get_swaggerui_blueprint


CODIGO_HTTP = {
	'OK': 200,
	'CREATED': 201,
	'NO_CONTENT': 204,
	'NOT_FOUND': 404,
	'BAD_REQUEST': 400
}

URL_PROYECTOS = 'https://mapache-proyectos.herokuapp.com/'

SEVERIDADES = {
    'alta': 7,
    'media': 30,
    'baja': 90
}

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PSA-SOPORTE"
    }
)

