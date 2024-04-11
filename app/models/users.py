from app import db, bcrypt, auth_manager
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from uuid import uuid4
from datetime import timezone
from .subjects import user_subjects_association
from .bookshelves import user_bookshelves_association
from app.utils.datetime_util import (
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
    utc_now,
)

from app.models.token_blacklist import BlacklistedToken
from flask_pyjwt import JWT


class User(db.Model):
    """
    User model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    last_logged_in = db.Column(db.DateTime, default=utc_now)
    is_email_confirmed = db.Column(db.Boolean, default=False)

    profile = db.relationship("Profile", uselist=False, back_populates="user")
    bookmarks = db.relationship("Bookmark", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    comment_votes = db.relationship("CommentVote", back_populates="user")
    ratings = db.relationship("Rating", back_populates="user")
    bookshelves = db.relationship("Bookshelf", back_populates="user")

    subjects = db.relationship(
        "Subject", secondary=user_subjects_association, back_populates="users"
    )
    bookshelves = db.relationship(
        "Bookshelf",
        secondary=user_bookshelves_association,
        back_populates="users",
    )

    public_id = db.Column(db.String, default=lambda: str(uuid4()))

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(
            self.created_at, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def last_logged_in_str(self):
        last_logged_in_utc = make_tzaware(
            self.last_logged_in, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(last_logged_in_utc, use_tz=get_local_utcoffset())

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.password_hash = hash_bytes.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_public_id(public_id):
        return User.query.filter_by(public_id=public_id).first()

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:

            auth_token = self.generate_auth_token()
            refresh_token = self.generate_refresh_token()
            return dict(
                auth_token=auth_token.signed,
                refresh_token=refresh_token.signed,
            )

        except Exception as e:
            return e

    def generate_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        return auth_manager.auth_token(
            {
                "public_id": self.public_id,
                "email": self.email,
            },
            dict(is_admin=self.is_admin),
        )

    def generate_refresh_token(self):
        """
        Generates the Refresh Token
        :return: string
        """
        return auth_manager.refresh_token(self.public_id)

    @classmethod
    def blacklist_token(cls, auth_token: JWT):
        """
        Adds a token to the blacklist
        :param token: string
        :return: Response
        """
        try:
            if auth_token:
                blacklist_token = BlacklistedToken(
                    token=auth_token.signed, expires_at=auth_token.exp
                )
                db.session.add(blacklist_token)
                db.session.commit()
                return dict(success=True)
            else:
                return dict(success=False, error="Invalid token")
        except Exception as e:
            return dict(success=False, error=str(e))

    def __repr__(self):
        return f"<User {self.email}>"
