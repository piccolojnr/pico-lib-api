from app import db


import enum
from datetime import timezone
from app.utils.datetime_util import (
    utc_now,
    localized_dt_string,
    get_local_utcoffset,
    make_tzaware,
)

from sqlalchemy.ext.hybrid import hybrid_property


class CommentVoteType(enum.Enum):
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"
    NONE = "none"


class CommentType(enum.Enum):
    COMMENT = "comment"
    REPLY = "reply"
    REVIEW = "review"


class CommentVote(db.Model):
    """
    A vote on a comment.
    """

    __tablename__ = "comment_votes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vote = db.Column(db.Enum(CommentVoteType), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))

    comment = db.relationship("Comment", back_populates="comment_votes")
    user = db.relationship("User", back_populates="comment_votes")

    @hybrid_property
    def created_at_str(self):
        created_str_utc = make_tzaware(self.created_at, timezone.utc, localize=False)
        return localized_dt_string(created_str_utc, get_local_utcoffset())

    @hybrid_property
    def updated_at_str(self):
        updated_str_utc = make_tzaware(self.updated_at, timezone.utc, localize=False)
        return localized_dt_string(updated_str_utc, get_local_utcoffset())

    def __repr__(self):
        return f"<CommentVote {self.id}>"


class Comment(db.Model):
    """
    A comment on a book.
    """

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    type = db.Column(db.Enum(CommentType), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id", ondelete="CASCADE"))
    rating = db.Column(db.Float, nullable=True)

    book = db.relationship("Book", back_populates="comments")
    user = db.relationship("User", back_populates="comments")
    parent = db.relationship("Comment", remote_side=[id], back_populates="replies")
    replies = db.relationship("Comment", back_populates="parent")
    comment_votes = db.relationship("CommentVote", back_populates="comment")

    @hybrid_property
    def type_str(self):
        return self.type.value

    @hybrid_property
    def number_of_replies(self):
        return len(self.replies)

    @hybrid_property
    def user_profile(self):
        return self.user.profile

    @hybrid_property
    def upvotes(self):
        return len(
            [vote for vote in self.comment_votes if vote.vote == CommentVoteType.UPVOTE]
        )

    @hybrid_property
    def downvotes(self):
        return len(
            [
                vote
                for vote in self.comment_votes
                if vote.vote == CommentVoteType.DOWNVOTE
            ]
        )

    @hybrid_property
    def created_at_str(self):
        created_str_utc = make_tzaware(self.created_at, timezone.utc, localize=False)
        return localized_dt_string(created_str_utc, get_local_utcoffset())

    @hybrid_property
    def updated_at_str(self):
        updated_str_utc = make_tzaware(self.updated_at, timezone.utc, localize=False)
        return localized_dt_string(updated_str_utc, get_local_utcoffset())

    @classmethod
    def get_by_id(cls, comment_id):
        return cls.query.filter(cls.id == comment_id).first()

    def __repr__(self):
        return f"<Comment {self.id}>"
