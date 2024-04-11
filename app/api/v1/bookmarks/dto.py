from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive
from app.api.v1.books.dto import book_model_short
from app.api.v1.user.dto import user_model
from datetime import datetime


def check_string_iso_format(date_string):
    try:
        datetime.fromisoformat(date_string)
        return date_string
    except ValueError:
        raise ValueError("Invalid ISO format")


bookmark_model = Model(
    "Bookmark",
    {
        "id": Integer,
        "status": String(attribute="status_str"),
        "book": Nested(book_model_short),
        "user": Nested(user_model),
    },
)

create_bookmark_reqparse = RequestParser(bundle_errors=True)
create_bookmark_reqparse.add_argument("book_id", type=str, required=True)
create_bookmark_reqparse.add_argument(
    "last_read", type=check_string_iso_format, required=False
)
create_bookmark_reqparse.add_argument(
    "status",
    type=str,
    choices=[
        "read",
        "unread",
        "want_to_read",
        "currently_reading",
        "READ",
        "UNREAD",
        "WANT_TO_READ",
        "CURRENTLY_READING",
    ],
    default="unread",
    required=True,
)

update_bookmark_reqparse = RequestParser(bundle_errors=True)
update_bookmark_reqparse.add_argument(
    "status",
    type=str,
    required=False,
    choices=[
        "read",
        "unread",
        "want_to_read",
        "currently_reading",
        "READ",
        "UNREAD",
        "WANT_TO_READ",
        "CURRENTLY_READING",
    ],
)

pagination_reqparse = RequestParser(bundle_errors=True)
pagination_reqparse.add_argument("page", type=positive, default=1, required=False)
pagination_reqparse.add_argument("per_page", type=positive, default=10, required=False)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)
bookmarks_pagination_model = Model(
    "BookmarkPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(bookmark_model)),
    },
)
