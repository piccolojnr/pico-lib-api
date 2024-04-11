from app import db

from sqlalchemy.ext.hybrid import hybrid_property

from app.utils.datetime_util import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)

from datetime import timezone
import enum


class BookmarkStatus(enum.Enum):
    """
    Bookmark status
    """

    READ = "read"
    UNREAD = "unread"
    WANT_TO_READ = "want to read"
    CURRENTLY_READING = "currently reading"


class Bookmark(db.Model):
    """
    Bookmark model
    """

    __tablename__ = "bookmarks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"))
    status = db.Column(
        db.Enum(BookmarkStatus), nullable=False, default=BookmarkStatus.UNREAD
    )
    last_read = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    user = db.relationship("User", back_populates="bookmarks")
    book = db.relationship("Book", back_populates="bookmarks")
    __table_args__ = (db.UniqueConstraint("user_id", "book_id"),)

    @hybrid_property
    def status_str(self):
        return self.status.value

    @hybrid_property
    def last_read_str(self):
        last_read_utc = make_tzaware(
            self.last_read, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(last_read_utc, use_tz=get_local_utcoffset())

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
        return f"<Bookmark {self.book_id} {self.status}>"

    def __init__(self, user_id, book_id, status, last_read=None):
        self.user_id = user_id
        self.book_id = book_id
        self.status = status
        self.last_read = last_read
