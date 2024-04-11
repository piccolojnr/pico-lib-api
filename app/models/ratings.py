from app import db

from datetime import timezone
from app.utils.datetime_util import (
    localized_dt_string,
    get_local_utcoffset,
    utc_now,
    make_tzaware,
)

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import UniqueConstraint


class Rating(db.Model):
    """
    Rating model
    """

    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=utc_now)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"))

    user = db.relationship("User", back_populates="ratings")
    book = db.relationship("Book", back_populates="ratings")

    __table_args__ = (
        UniqueConstraint("user_id", "book_id", name="unique_user_book_rating"),
    )

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(self.created_at, timezone.utc, localize=False)
        return localized_dt_string(created_at_utc, get_local_utcoffset())

    def __repr__(self):
        return f"<Rating {self.user_id} {self.book_id} {self.review_id} {self.rating}>"

    def __init__(self, rating, user_id, book_id=None):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
