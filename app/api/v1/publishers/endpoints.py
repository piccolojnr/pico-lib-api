from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from http import HTTPStatus
from .dto import (
    pagination_links_model,
    pagination_reqparse,
    create_publisher_reqparse,
    publishers_pagination_model,
    publisher_model,
    update_publisher_reqparse,
)
from .business import (
    process_create_publisher,
    process_delete_publisher,
    process_get_publisher,
    process_update_publisher,
    process_get_publishers,
    process_delete_publisher_book,
    process_create_publisher_book,
    process_get_publisher_books,
)

publisher_ns = Namespace(name="publishers", validate=True)
publisher_ns.models[publisher_model.name] = publisher_model
publisher_ns.models[publishers_pagination_model.name] = publishers_pagination_model
publisher_ns.models[pagination_links_model.name] = pagination_links_model


@publisher_ns.route("/", endpoint="publishers")
class PublishersResource(Resource):
    @publisher_ns.expect(pagination_reqparse)
    def get(self):
        """
        Get  books publisher.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_publishers(page, per_page)

    @require_token(scope={"is_admin": True})
    @publisher_ns.expect(create_publisher_reqparse, validate=True)
    @publisher_ns.doc(security="Bearer")
    @publisher_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @publisher_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @publisher_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        """
        Create  books publisher.
        """
        args = create_publisher_reqparse.parse_args()
        name = args["name"]
        return process_create_publisher(name)


@publisher_ns.route("/<publisher_id>", endpoint="publisher")
class ResourceResource(Resource):
    @publisher_ns.marshal_with(publisher_model)
    def get(self, publisher_id):
        """
        Get  book publisher.
        """
        return process_get_publisher(publisher_id)

    @require_token(scope={"is_admin": True})
    @publisher_ns.doc(security="Bearer")
    @publisher_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @publisher_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @publisher_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, publisher_id):
        """
        Delete  book publisher.
        """
        return process_delete_publisher(publisher_id)

    @require_token(scope={"is_admin": True})
    @publisher_ns.doc(security="Bearer")
    @publisher_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @publisher_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @publisher_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @publisher_ns.expect(update_publisher_reqparse)
    def put(self, publisher_id):
        """
        Update  book publisher.
        """
        args = update_publisher_reqparse.parse_args()
        name = args["name"]
        return process_update_publisher(publisher_id, name)


@publisher_ns.route("/<publisher_id>/books", endpoint="publisher_books")
class PublisherBooksResource(Resource):
    @publisher_ns.expect(pagination_reqparse)
    def get(self, publisher_id):
        """
        Get publisher's books.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_publisher_books(publisher_id, page, per_page)


@publisher_ns.route("/<publisher_id>/books/<book_id>", endpoint="publisher_book")
class PublisherBookResource(Resource):
    @require_token(scope={"is_admin": True})
    @publisher_ns.doc(security="Bearer")
    @publisher_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @publisher_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @publisher_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, publisher_id, book_id):
        """
        Delete publisher's book.
        """
        return process_delete_publisher_book(publisher_id, book_id)

    @require_token(scope={"is_admin": True})
    @publisher_ns.doc(security="Bearer")
    @publisher_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @publisher_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @publisher_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, publisher_id, book_id):
        """
        Create publisher's book.
        """
        return process_create_publisher_book(publisher_id, book_id)
