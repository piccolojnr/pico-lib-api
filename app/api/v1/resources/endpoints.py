from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from flask import request
from http import HTTPStatus
from .dto import (
    book_model_short,
    pagination_links_model,
    pagination_reqparse,
    resource_model,
    resources_pagination_model,
    short_resource_model,
    create_resource_model,
)
from .business import (
    process_create_resource,
    process_delete_resource,
    process_get_resource,
    process_update_resource,
    process_get_resources,
)

resources_ns = Namespace(name="resources", validate=True)
resources_ns.models[book_model_short.name] = book_model_short
resources_ns.models[pagination_links_model.name] = pagination_links_model
resources_ns.models[resource_model.name] = resource_model
resources_ns.models[resources_pagination_model.name] = resources_pagination_model
resources_ns.models[short_resource_model.name] = short_resource_model
resources_ns.models[create_resource_model.name] = create_resource_model


@resources_ns.route("/<book_id>", endpoint="resources")
class ResourcesResource(Resource):
    @resources_ns.expect(pagination_reqparse)
    def get(self, book_id):
        """
        Get  books resources.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_resources(book_id, page, per_page)

    @require_token(scope={"is_admin": True})
    @resources_ns.expect(create_resource_model, validate=True)
    @resources_ns.doc(security="Bearer")
    @resources_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @resources_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @resources_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, book_id):
        """
        Create  books resource.
        """
        data = request.get_json()

        return process_create_resource(book_id, data)


@resources_ns.route("/resource/<resource_id>", endpoint="resource")
class ResourceResource(Resource):
    @resources_ns.marshal_with(resource_model)
    def get(self, resource_id):
        """
        Get  book resource.
        """
        return process_get_resource(resource_id)

    @require_token(scope={"is_admin": True})
    @resources_ns.doc(security="Bearer")
    @resources_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @resources_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @resources_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, resource_id):
        """
        Delete  book resource.
        """
        return process_delete_resource(resource_id)

    @require_token(scope={"is_admin": True})
    @resources_ns.doc(security="Bearer")
    @resources_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @resources_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @resources_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self, resource_id):
        """
        Update  book resource.
        """
        data = request.get_json()
        return process_update_resource(resource_id, data)
