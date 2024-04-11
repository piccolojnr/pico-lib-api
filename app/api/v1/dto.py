from flask_restx.reqparse import RequestParser
from flask_restx import fields, inputs, Model

from app.api.v1 import api


from .agents.dto import (
    agent_model,
    agent_pagination_model,
    pagination_reqparse,
    create_agent_reqparse,
)
from .auth.dto import (
    auth_change_password_reqparser,
    auth_login_reqparser,
    auth_register_reqparser,
)
from .bookmarks.dto import (
    bookmark_model,
    create_bookmark_reqparse,
    bookmarks_pagination_model,
    update_bookmark_reqparse,
)
from .books.dto import (
    book_model,
    book_pagination_model,
    pagination_reqparse,
    book_model_short,
    create_book_model,
    pagination_reqparse,
    update_book_model,
)
from .bookshelves.dto import (
    bookshelf_model,
    bookshelf_pagination_model,
    create_bookshelf_model,
    pagination_reqparser,
    short_bookshelf_model,
    update_bookshelf_model,
)
from .comments.dto import (
    comment_model,
    comment_pagination_model,
    retrieve_comments_reqparse,
)
from .languages.dto import (
    create_language_reqparse,
    languages_pagination_model,
    langauge_model,
    update_language_reqparse,
)
from .publishers.dto import (
    create_publisher_reqparse,
    publisher_model,
    publishers_pagination_model,
    update_publisher_reqparse,
)
from .resources.dto import (
    create_resource_model,
    resource_model,
    resources_pagination_model,
    short_resource_model,
)
from .subjects.dto import (
    create_subject_parser,
    subject_model,
    subject_pagination_model,
    update_subject_parser,
)
from .user.dto import profile_model, short_profile_model, user_model

pagination_reqparse = RequestParser(bundle_errors=True)
pagination_reqparse.add_argument(
    "page", type=inputs.positive, default=1, required=False
)
pagination_reqparse.add_argument(
    "per_page",
    type=inputs.positive,
    default=10,
    required=False,
)

pagination_links_model = Model(
    "Nav Links",
    {
        "self": fields.String,
        "prev": fields.String,
        "next": fields.String,
        "first": fields.String,
        "last": fields.String,
    },
)
api.models[pagination_links_model.name] = pagination_links_model

__all__ = [
    "create_language_reqparse",
    "short_bookshelf_model",
    "update_bookshelf_model",
    "auth_login_reqparser",
    "update_book_model",
    "create_publisher_reqparse",
    "agent_pagination_model",
    "update_subject_parser",
    "profile_model",
    "subject_pagination_model",
    "create_bookmark_reqparse",
    "agent_model",
    "short_resource_model",
    "pagination_reqparse",
    "pagination_reqparse",
    "user_model",
    "comment_model",
    "create_subject_parser",
    "create_agent_reqparse",
    "book_model",
    "resource_model",
    "update_bookmark_reqparse",
    "langauge_model",
    "create_resource_model",
    "book_pagination_model",
    "bookshelf_model",
    "update_publisher_reqparse",
    "auth_register_reqparser",
    "create_bookshelf_model",
    "bookshelf_pagination_model",
    "languages_pagination_model",
    "bookmarks_pagination_model",
    "pagination_reqparse",
    "book_model_short",
    "pagination_reqparser",
    "publisher_model",
    "short_profile_model",
    "update_language_reqparse",
    "retrieve_comments_reqparse",
    "create_book_model",
    "subject_model",
    "publishers_pagination_model",
    "comment_pagination_model",
    "bookmark_model",
    "auth_change_password_reqparser",
    "resources_pagination_model",
]
