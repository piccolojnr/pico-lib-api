from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive
from app.api.v1.user.dto import user_model


subject_model = Model(
    "Subject",
    {
        "id": Integer,
        "name": String,
        "score": Integer,
    },
)

user_subject_model = Model(
    "UserSubject",
    {
        "id": Integer,
        "user": Nested(user_model),
        "subject": Nested(subject_model),
    },
)


create_subject_parser = RequestParser()
create_subject_parser.add_argument(
    "name", type=str, required=True, help="Subject name is required"
)
create_subject_parser.add_argument("score", type=positive, required=False)

update_subject_parser = RequestParser()
update_subject_parser.add_argument("name", type=str, required=False)
update_subject_parser.add_argument("score", type=positive, required=False)


pagination_reqparse = RequestParser(bundle_errors=True)
pagination_reqparse.add_argument("page", type=positive, default=1, required=False)
pagination_reqparse.add_argument("per_page", type=positive, default=10, required=False)
pagination_reqparse.add_argument("q", type=str, default="", required=False)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)
subject_pagination_model = Model(
    "SubjectPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(subject_model)),
    },
)
