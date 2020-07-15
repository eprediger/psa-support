from flask_swagger_ui import get_swaggerui_blueprint


CODIGO_HTTP_OK = 200
CODIGO_HTTP_NO_CONTENT = 204
CODIGO_HTTP_NOT_FOUND = 404
CODIGO_HTTP_BAD_REQUEST = 400

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

