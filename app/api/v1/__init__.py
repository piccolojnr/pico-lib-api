"""API blueprint configuration."""

# Import necessary modules and classes
from flask import Blueprint, jsonify
from flask_restx import Api

# Import endpoints from different namespaces
from .auth.endpoints import auth_ns
from .user.endpoints import user_ns
from .comments.endpoints import comments_ns
from .books.endpoints import books_ns
from .agents.endpoints import agents_ns
from .bookshelves.endpoints import bookshelves_ns
from .resources.endpoints import resources_ns
from .subjects.endpoints import subjects_ns
from .languages.endpoints import language_ns
from .publishers.endpoints import publisher_ns
from .bookmarks.endpoints import bookmark_ns
from .token.endpoints import token_ns

# Define the API blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

# Define authorizations for Swagger UI
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

# Create an instance of Flask-RestX API
api = Api(
    api_bp,
    version="1.0",
    title="Flask API with JWT-Based Authentication",
    description="Welcome to the Swagger UI documentation for the Widget API",
    doc="/ui",
    authorizations=authorizations,
)


# Define the root route for the API
@api_bp.route("/")
def index():
    return jsonify(
        {
            "message": "Welcome to the Pico-Library Flask API version 1 with JWT-Based Authentication",
            "author": "piccolosan",
            "endpoints": [
                "/auth",
                "/user",
                "/comments",
                "/books",
                "/agents",
                "/bookshelves",
                "/resources",
            ],
        }
    )


# Add namespaces (API endpoints) to the API
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(user_ns, path="/user")
api.add_namespace(comments_ns, path="/comments")
api.add_namespace(books_ns, path="/books")
api.add_namespace(agents_ns, path="/agents")
api.add_namespace(bookshelves_ns, path="/bookshelves")
api.add_namespace(resources_ns, path="/resources")
api.add_namespace(subjects_ns, path="/subjects")
api.add_namespace(language_ns, path="/languages")
api.add_namespace(publisher_ns, path="/publishers")
api.add_namespace(bookmark_ns, path="/bookmarks")
api.add_namespace(token_ns, path="/clear_tokens")
