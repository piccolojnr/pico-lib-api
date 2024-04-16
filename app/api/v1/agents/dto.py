from flask_restx import Model
from flask_restx.fields import String, Integer, Boolean, Nested, List
from flask_restx.reqparse import RequestParser
from flask_restx.inputs import positive

# Request parser for pagination
pagination_reqparse = RequestParser(bundle_errors=True)
pagination_reqparse.add_argument(
    "page", type=positive, required=False, default=1, help="Page number"
)
pagination_reqparse.add_argument(
    "per_page",
    type=positive,
    required=False,
    default=10,
    help="Items per page",
)
pagination_reqparse.add_argument("q", type=str, required=False, help="Search query")
pagination_reqparse.add_argument(
    "type",
    type=str,
    choices=[
        "ANNOTATOR",
        "AUTHOR",
        "COMMENTATOR",
        "COMPILER",
        "COMPOSER",
        "CONTRIBUTOR",
        "EDITOR",
        "ILLUSTRATOR",
        "OTHER",
        "PHOTOGRAPHER",
        "TRANSLATOR",
        "annotator",
        "author",
        "commentator",
        "compiler",
        "composer",
        "contributor",
        "editor",
        "illustrator",
        "other",
        "photographer",
        "translator",
    ],
    required=False,
    help="Agent type",
)

# Model for short book representation
book_model_short = Model(
    "BookShort",
    {
        "id": Integer,
        "title": String,
        "format": String,
        "description": String,
        "image": String,
        "license": String,
        "downloads": Integer,
        "created_at": String(attribute="created_at_str"),
        "updated_at": String(attribute="updated_at_str"),
    },
)

# Model for representing an agent
agent_model = Model(
    "Agent",
    {
        "id": Integer,
        "name": String,
        "alias": String,
        "agent_books": List(Nested(book_model_short)),
        "birth_date": String,
        "death_date": String,
        "webpage": String,
        "agent_type": String,
    },
)

# Shortened model for representing an agent
short_agent_model = Model(
    "ShortAgent",
    {
        "id": Integer,
        "name": String,
        "alias": String,
        "birth_date": String,
        "death_date": String,
        "webpage": String,
        "agent_type": String,
    },
)

# Request parser for creating an agent
create_agent_reqparse = RequestParser(bundle_errors=True)
create_agent_reqparse.add_argument(
    "name", type=str, required=True, help="Agent name is required"
)
create_agent_reqparse.add_argument(
    "alias",
    type=str,
    required=False,
)
create_agent_reqparse.add_argument(
    "birth_date",
    type=str,
    required=False,
)
create_agent_reqparse.add_argument(
    "death_date", type=str, required=False, help="Agent death date is optional"
)
create_agent_reqparse.add_argument(
    "webpage", type=str, required=False, help="Agent webpage is optional"
)
create_agent_reqparse.add_argument(
    "type",
    type=str,
    choices=[
        "ANNOTATOR",
        "AUTHOR",
        "COMMENTATOR",
        "COMPILER",
        "COMPOSER",
        "CONTRIBUTOR",
        "EDITOR",
        "ILLUSTRATOR",
        "OTHER",
        "PHOTOGRAPHER",
        "TRANSLATOR",
        "annotator",
        "author",
        "commentator",
        "compiler",
        "composer",
        "contributor",
        "editor",
        "illustrator",
        "other",
        "photographer",
        "translator",
    ],
    required=False,
)

# Model for pagination links
pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

# Model for paginated list of agents
agent_pagination_model = Model(
    "AgentPagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer,
        "items_per_page": Integer,
        "total_items": Integer,
        "items": List(Nested(short_agent_model)),
    },
)
