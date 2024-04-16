# Import necessary modules and packages
from app import create_app, db  # Importing create_app function and database instance
from app.models import User, Book  # Importing User and Book models
import os  # Importing os module


# Create Flask application instance based on environment variable
app = create_app(os.environ.get("FLASK_ENV", "development"))  # Creating Flask app
app.app_context().push()  # Pushing application context


# Define shell context processor to make database and models available in shell
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Book": Book,
    }  # Returning database and models for shell context
