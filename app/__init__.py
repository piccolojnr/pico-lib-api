from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import get_config
from flask_pyjwt import AuthManager, current_token
from http import HTTPStatus
from flask_restx import abort
from flask_mail import Mail

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
auth_manager = AuthManager()
mail = Mail()


def create_app(config_name):
    app = Flask("pico-library-api")
    app.debug = False
    app.config.from_object(get_config(config_name))

    from app.api.v1 import api_bp

    app.register_blueprint(api_bp)

    @app.before_request
    def check_blacklist():
        if current_token:
            from app.models import BlacklistedToken

            token = BlacklistedToken.check_blacklist(current_token.signed)
            if token:
                abort(HTTPStatus.UNAUTHORIZED, "Unauthorized")

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    auth_manager.init_app(app)
    mail.init_app(app)

    return app
