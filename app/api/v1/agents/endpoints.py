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
    short_agent_model,
)

agents_ns = Namespace(name="agents", validate=True)
agents_ns.models[agent_model.name] = agent_model
agents_ns.models[short_agent_model.name] = short_agent_model
agents_ns.models[pagination_links_model.name] = pagination_links_model
agents_ns.models[agent_pagination_model.name] = agent_pagination_model


@agents_ns.route("/", endpoint="agents")
class AgentsResource(Resource):
    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @agents_ns.expect(create_agent_reqparse)
    def post(self):
        args = create_agent_reqparse.parse_args()
        return process_create_agent(args)

    @agents_ns.expect(pagination_reqparse)
    def get(self):
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        type = args["type"]
        q = args["q"]
        return process_get_agents(page=page, per_page=per_page, type=type, q=q)


@agents_ns.route("/<int:agent_id>", endpoint="agent")
class AgentResource(Resource):

    @agents_ns.marshal_with(agent_model)
    def get(self, agent_id):
        """
        Get agent.
        """
        return process_get_agent(agent_id)

    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, agent_id):
        """
        Delete agent.
        """
        return process_delete_agent(agent_id)

    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @agents_ns.expect(create_agent_reqparse)
    def put(self, agent_id):
        """
        Update agent.
        """
        args = create_agent_reqparse.parse_args()
        return process_update_agent(agent_id, args)


@agents_ns.route("/<int:agent_id>/books/<int:book_id>", endpoint="agent_book")
class AgentBookResource(Resource):
    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, agent_id, book_id):
        """
        Delete agent's book.
        """
        return process_remove_agent_book(agent_id, book_id)

    @require_token(scope={"is_admin": True})
    @agents_ns.doc(security="Bearer")
    @agents_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @agents_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @agents_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, agent_id, book_id):
        """
        Create agent's book.
        """
        return process_add_agent_book(agent_id, book_id)


@agents_ns.route("/popular", endpoint="popular_agents")
class PopularAgentsResource(Resource):
    @agents_ns.expect(pagination_reqparse)
    def get(self):
        """
        Get popular agents.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_popular_agents(page, per_page)
