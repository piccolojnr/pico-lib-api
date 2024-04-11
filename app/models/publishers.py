from app import db

from sqlalchemy.ext.hybrid import hybrid_property

book_publishers_association = db.Table(
    "book_publishers",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "publisher_id", db.String, db.ForeignKey("publishers.name", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "publisher_id"),
)


class Publisher(db.Model):
    """
    Publisher model
    """

    __tablename__ = "publishers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    books = db.relationship(
        "Book", secondary=book_publishers_association, back_populates="publishers"
    )

    @hybrid_property
    def number_of_books(self):
        return len(self.books)

    def __repr__(self):
        return f"<Publisher(name={self.name})>"

    def __init__(self, name):
        self.name = name
