from flask import Flask
import os
from blueprints import user, login, config
import models
from utils.error_handler import error_treatment


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='{}://{}:{}@{}:{}/{}'.format(
            os.environ.get('DB_CONNECTOR'),
            os.environ.get('DB_USERNAME'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            os.environ.get('DB_PORT'),
            os.environ.get('DB_NAME')
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    if config:
        app.config.from_mapping(**config)

    models.db.init_app(app=app)
    models.migrate.init_app(app=app)

    error_treatment(app=app)

    # NOTE register blueprints
    app.register_blueprint(user.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(config.bp)

    # NOTE CORS
    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        header['Access-Control-Allow-Methods'] = '*'
        header['Access-Control-Allow-Headers'] = '*'
        return response

    return app
