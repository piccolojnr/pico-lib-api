from app import db


from datetime import timezone
from app.utils.datetime_util import (
    localized_dt_string,
    get_local_utcoffset,
    utc_now,
    make_tzaware,
)

from sqlalchemy.ext.hybrid import hybrid_property


class ResourceType(db.Model):
    """ """

    __tablename__ = "resource_type"
    name = db.Column(db.String, primary_key=True)

    resources = db.relationship("Resource", back_populates="type")


class Resource(db.Model):
    """ """

    __tablename__ = "resources"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String, unique=True, nullable=False)
    size = db.Column(db.Integer)
    modified = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    type_name = db.Column(
        db.String, db.ForeignKey("resource_type.name", ondelete="CASCADE")
    )
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"))

    type = db.relationship("ResourceType", back_populates="resources")
    book = db.relationship("Book", back_populates="resources")

    __table_args__ = (db.UniqueConstraint("url", "type_name"),)

    @hybrid_property
    def type_str(self):
        return self.type.name

    @hybrid_property
    def modified_str(self):
        modified_utc = make_tzaware(self.modified, timezone.utc, localize=False)
        return localized_dt_string(modified_utc, get_local_utcoffset())

    def __repr__(self):
        return f"<Resource {self.url}>"
