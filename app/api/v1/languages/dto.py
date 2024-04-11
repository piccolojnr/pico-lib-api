from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive

langauge_model = Model(
    "Language",
    {
        "id": Integer,
        "name": String,
        "code": String,
        "number_of_books": Integer,
    },
)

create_language_reqparse = RequestParser(bundle_errors=True)
create_language_reqparse.add_argument("code", type=str, required=True)
create_language_reqparse.add_argument("name", type=str, required=False)

update_language_reqparse = RequestParser(bundle_errors=True)
update_language_reqparse.add_argument("code", type=str, required=False)
update_language_reqparse.add_argument("name", type=str, required=False)

pagination_reqparse = RequestParser(bundle_errors=True)
pagination_reqparse.add_argument("page", type=positive, default=1, required=False)
pagination_reqparse.add_argument("per_page", type=positive, default=10, required=False)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)
languages_pagination_model = Model(
    "LanguagePagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(langauge_model)),
    },
)
