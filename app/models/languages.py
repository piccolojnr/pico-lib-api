from app import db
from sqlalchemy.ext.hybrid import hybrid_property

book_languages_association = db.Table(
    "book_languages",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "language_id", db.Integer, db.ForeignKey("languages.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "language_id"),
)


class Language(db.Model):
    """
    Language model
    """

    __tablename__ = "languages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)

    books = db.relationship(
        "Book", secondary=book_languages_association, back_populates="languages"
    )

    @hybrid_property
    def number_of_books(self):
        return len(self.books)

    def __repr__(self):
        return f"<Language {self.code}>"
