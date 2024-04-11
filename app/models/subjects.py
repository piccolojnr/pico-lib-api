from app import db

book_subjects_association = db.Table(
    "book_subjects",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "subject_id", db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "subject_id"),
)

user_subjects_association = db.Table(
    "user_subjects",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")),
    db.Column(
        "subject_id", db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("user_id", "subject_id"),
)


class Subject(db.Model):
    """
    Subject models
    """

    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)

    books = db.relationship(
        "Book", secondary=book_subjects_association, back_populates="subjects"
    )
    users = db.relationship(
        "User", secondary=user_subjects_association, back_populates="subjects"
    )

    def __repr__(self):
        return f"<Subject(name={self.name})>"
