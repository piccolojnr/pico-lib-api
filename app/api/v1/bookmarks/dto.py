from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List, Raw
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive
from app.api.v1.user.dto import user_model
from datetime import datetime
from flask_pyjwt import current_token
from app.models import User, Bookmark


def check_string_iso_format(date_string):
    try:
        datetime.fromisoformat(date_string)
        return date_string
    except ValueError:
        raise ValueError("Invalid ISO format")


def get_bookmark(book):
    public_id = current_token.sub["public_id"]
    user = User.find_by_public_id(public_id)
    bookmark = Bookmark.query.filter(
        Bookmark.book_id == book.id, Bookmark.user_id == user.id
    ).first()
    if bookmark:
        return bookmark.status_str
    return None


bookmark_book_model = Model(
    "BookmarkBook",
    {
        "id": Integer,
        "title": String,
        "format": String,
        "downloads": Integer,
        "image": String,
        "bookmark": Raw(attribute=lambda book: get_bookmark(book)),
    },
)

bookmark_model = Model(
    "Bookmark",
    {
        "id": Integer,
        "status": String(attribute="status_str"),
        "user": Nested(user_model),
    },
)

create_bookmark_reqparse = RequestParser(bundle_errors=True)
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
    ],
)

pagination_reqparse = RequestParser(bundle_errors=True)
pagination_reqparse.add_argument("page", type=positive, default=1, required=False)
pagination_reqparse.add_argument("per_page", type=positive, default=10, required=False)
pagination_reqparse.add_argument(
    "status",
    type=str,
    choices=[
        "read",
        "unread",
        "want_to_read",
        "currently_reading",
    ],
    required=False,
)


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

bookmark_books_pagination_model = Model(
    "BookmarkBooksPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(bookmark_book_model)),
    },
)
