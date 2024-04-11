from app import create_app, db
from app.models import User, Book
import os


app = create_app(os.environ.get("FLASK_ENV"))
app.app_context().push()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Book": Book}
