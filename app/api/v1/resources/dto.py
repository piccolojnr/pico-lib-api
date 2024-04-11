from datetime import datetime
from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive

book_model_short = Model(
    "BookShort",
    {
        "id": Integer,
        "title": String,
        "format": String,
        "description": String,
        "license": String,
        "downloads": Integer,
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
    },
)

resource_model = Model(
    "Resource",
    {
        "id": Integer,
        "url": String,
        "size": Integer,
        "modified": String(attribute="modified_str"),
        "type": String(attribute="type_str"),
        "book": Nested(book_model_short),
    },
)
short_resource_model = Model(
    "ShortResource",
    {
        "id": Integer,
        "url": String,
        "size": Integer,
        "modified": String(attribute="modified_str"),
        "type": String(attribute="type_str"),
        "book_id": Integer,
    },
)

create_resource_model = Model(
    "CreateResource",
    {
        "url": String(required=True),
        "size": Integer,
        "modified": String,
        "type": String,
    },
)


pagination_reqparse = RequestParser(bundle_errors=True)
pagination_reqparse.add_argument("page", type=positive, default=1, required=False)
pagination_reqparse.add_argument("per_page", type=positive, default=10, required=False)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)
resources_pagination_model = Model(
    "ResourcePagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(short_resource_model)),
    },
)
