from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from http import HTTPStatus
from app.api.v1.agents.business import (
    process_get_agents,
    process_create_agent,
    process_get_agent,
    process_delete_agent,
    process_update_agent,
    process_add_agent_book,
    process_remove_agent_book,
    process_get_popular_agents,
)
from app.api.v1.agents.dto import (
    agent_model,
    short_agent_model,
    create_agent_reqparse,
    pagination_links_model,
    agent_pagination_model,
    pagination_reqparse,
)

# Create a namespace for agents
agents_ns = Namespace(name="agents", validate=True)
# Register models with the namespace
agents_ns.models[agent_model.name] = agent_model
agents_ns.models[short_agent_model.name] = short_agent_model
agents_ns.models[pagination_links_model.name] = pagination_links_model
agents_ns.models[agent_pagination_model.name] = agent_pagination_model


# Define endpoints for agents
@agents_ns.route("/", endpoint="agents")
class AgentsResource(Resource):
    # Endpoint for creating a new agent
    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @agents_ns.expect(create_agent_reqparse)
    def post(self):
        args = create_agent_reqparse.parse_args()
        return process_create_agent(args)

    # Endpoint for getting a list of agents with pagination and filtering
    @agents_ns.expect(pagination_reqparse)
    def get(self):
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        type = args["type"]
        q = args["q"]
        return process_get_agents(page=page, per_page=per_page, type=type, q=q)


# Define endpoints for individual agents
@agents_ns.route("/<int:agent_id>", endpoint="agent")
class AgentResource(Resource):
    # Endpoint for getting an individual agent
    @agents_ns.marshal_with(agent_model)
    def get(self, agent_id):
        return process_get_agent(agent_id)

    # Endpoint for deleting an individual agent
    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, agent_id):
        return process_delete_agent(agent_id)

    # Endpoint for updating an individual agent
    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @agents_ns.expect(create_agent_reqparse)
    def put(self, agent_id):
        args = create_agent_reqparse.parse_args()
        return process_update_agent(agent_id, args)


# Define endpoints for agent's books
@agents_ns.route("/<int:agent_id>/books/<int:book_id>", endpoint="agent_book")
class AgentBookResource(Resource):
    # Endpoint for deleting an agent's book
    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, agent_id, book_id):
        return process_remove_agent_book(agent_id, book_id)

    # Endpoint for adding an agent's book
    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, agent_id, book_id):
        return process_add_agent_book(agent_id, book_id)


# Endpoint for getting popular agents
@agents_ns.route("/popular", endpoint="popular_agents")
class PopularAgentsResource(Resource):
    # Endpoint for getting popular agents with pagination
    @agents_ns.expect(pagination_reqparse)
    def get(self):
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_popular_agents(page, per_page)
