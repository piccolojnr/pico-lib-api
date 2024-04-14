from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Float, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive
from app.api.v1.user.dto import short_profile_model

comment_model = Model(
    "Comment",
    {
        "id": Integer,
        "content": String,
        "type": String(attribute="type_str"),
        "user_profile": Nested(short_profile_model),
        "book_id": Integer,
        "parent_id": Integer,
        "rating": Float,
        "upvotes": Integer,
        "downvotes": Integer,
        "number_of_replies": Integer,
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
    },
)

create_comment_model = Model(
    "CreateComment",
    {
        "type": String,
        "content": String,
        "book_id": Integer,
        "parent_id": Integer,
        "rating": Float,
    },
)


pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

comment_pagination_model = Model(
    "CommentPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(comment_model)),
    },
)

retrieve_comments_reqparse = RequestParser(bundle_errors=True)
retrieve_comments_reqparse.add_argument("public_id", type=str, required=False)

retrieve_comments_reqparse.add_argument("book_id", type=str, required=False)
retrieve_comments_reqparse.add_argument("parent_id", type=str, required=False)
retrieve_comments_reqparse.add_argument(
    "type",
    type=str,
    choices=["comment", "reply", "review"],
    required=True,
    default="comment",
)
retrieve_comments_reqparse.add_argument(
    "page", type=positive, default=1, required=False
)
retrieve_comments_reqparse.add_argument(
    "per_page", type=positive, default=10, required=False
)

vote_comment_req_parse = RequestParser(bundle_errors=True)
vote_comment_req_parse.add_argument(
    "vote_type", type=str, choices=["upvote", "downvote"], default="upvote"
)
