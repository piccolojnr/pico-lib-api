from flask_restx.reqparse import RequestParser
from flask_restx.fields import String, Integer, Boolean, Nested, List
from flask_restx import Model


create_bookshelf_model = Model(
    "CreateBookshelf",
    {
        "name": String(required=True),
        "description": String,
        "cover_image": String,
        "is_public": Boolean,
    },
)


update_bookshelf_model = create_bookshelf_model.inherit(
    "UpdateBookshelf",
    {
        "name": String,
        "description": String,
        "cover_image": String,
        "is_public": Boolean,
        "score": Integer,
    },
)
short_bookshelf_model = Model(
    "ShortBookShelf",
    {
        "id": Integer,
        "name": String,
        "cover_image": String,
        "is_public": Boolean,
        "score": Integer,
    },
)

bookshelf_model = Model(
    "BookShelf",
    {
        "id": Integer,
        "name": String,
        "description": String,
        "cover_image": String,
        "is_public": Boolean,
        "score": Integer,
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
    },
)
pagination_reqparser = RequestParser()
pagination_reqparser.add_argument("page", type=int, default=1)
pagination_reqparser.add_argument("per_page", type=int, default=10)
pagination_reqparser.add_argument("q", type=str, default="", required=False)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

bookshelf_pagination_model = Model(
    "BookshelfPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(short_bookshelf_model)),
    },
)
