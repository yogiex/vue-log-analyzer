from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from routes.api import api_bp
from routes.main import main_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Konfigurasi Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # semua route
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"   # URL untuk UI Swagger
    }

    swagger_template = {
        "info": {
            "title": "EPrT Log Analyzer API",
            "description": "API untuk monitoring dan deteksi kecurangan ujian EPrT pada LMS Moodle",
            "version": "1.0.0",
            "contact": {
                "name": "Proctor Team",
                "email": "proctor@example.com"
            }
        },
        "securityDefinitions": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key"
            }
        }
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # Register Blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8443, debug=True)