from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import get_config
from flask_pyjwt import AuthManager, current_token
from http import HTTPStatus
from flask_restx import abort
from flask_mail import Mail

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
auth_manager = AuthManager()
mail = Mail()


def create_app(config_name):
    # Create Flask application instance
    app = Flask("pico-library-api")
    app.debug = False  # Set debug mode to False
    app.config.from_object(get_config(config_name))  # Load configuration settings

    # Import API blueprint and register it with the application
    from app.api.v1 import api_bp

    app.register_blueprint(api_bp)

    # Function to run before each request to check for blacklisted tokens
    @app.before_request
    def check_blacklist():
        if current_token:
            from app.models import BlacklistedToken

            # Check if the token is blacklisted
            token = BlacklistedToken.check_blacklist(current_token.signed)
            if token:
                abort(HTTPStatus.UNAUTHORIZED, "Unauthorized")

    # Enable CORS for API routes
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["Authorization", "Content-Type"],
            }
        },
    )

    # Initialize Flask extensions with the application instance
    db.init_app(app)
    migrate.init_app(app)
    bcrypt.init_app(app)
    auth_manager.init_app(app)
    mail.init_app(app)

    # Define a route for the root endpoint
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to Pico Library API"})

    return app  # Return the Flask application instance
