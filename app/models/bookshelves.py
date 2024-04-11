from datetime import timezone
from app import db
from app.utils.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)
from sqlalchemy.ext.hybrid import hybrid_property


book_bookshelves_association = db.Table(
    "book_bookshelves",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE")),
    db.Column(
        "bookshelf_id", db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("book_id", "bookshelf_id"),
)


user_bookshelves_association = db.Table(
    "user_bookshelves",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")),
    db.Column(
        "bookshelf_id", db.Integer, db.ForeignKey("bookshelves.id", ondelete="CASCADE")
    ),
    db.PrimaryKeyConstraint("user_id", "bookshelf_id"),
)


class Bookshelf(db.Model):
    """
    Bookshelf model
    """

    __tablename__ = "bookshelves"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    score = db.Column(db.Integer, default=0)
    cover_image = db.Column(db.String)
    description = db.Column(db.String)
    score = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    user = db.relationship("User", back_populates="bookshelves")

    books = db.relationship(
        "Book", secondary=book_bookshelves_association, back_populates="bookshelves"
    )
    users = db.relationship(
        "User", secondary=user_bookshelves_association, back_populates="bookshelves"
    )

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def updated_at_str(self):
        updated_at_utc = make_tzaware(
            self.updated_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(updated_at_utc, use_tz=get_local_utcoffset())

    def __repr__(self):
        return f"<Bookshelf {self.name}>"
