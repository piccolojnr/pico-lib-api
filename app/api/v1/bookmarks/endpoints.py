from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from http import HTTPStatus
from .dto import (
    pagination_links_model,
    pagination_reqparse,
    create_bookmark_reqparse,
    bookmarks_pagination_model,
    bookmark_model,
    update_bookmark_reqparse,
)
from .business import (
    process_create_bookmark,
    process_delete_bookmark,
    process_get_bookmark,
    process_update_bookmark,
    process_get_bookmarks,
)

bookmark_ns = Namespace(name="bookmarks", validate=True)
bookmark_ns.models[bookmark_model.name] = bookmark_model
bookmark_ns.models[bookmarks_pagination_model.name] = bookmarks_pagination_model
bookmark_ns.models[pagination_links_model.name] = pagination_links_model


@bookmark_ns.route("/", endpoint="bookmarks")
class PublishersResource(Resource):
    @bookmark_ns.expect(pagination_reqparse)
    def get(self):
        """
        Get  books bookmark.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_bookmarks(page, per_page)

    @require_token()
    @bookmark_ns.expect(create_bookmark_reqparse, validate=True)
    @bookmark_ns.doc(security="Bearer")
    @bookmark_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookmark_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookmark_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        """
        Create  books bookmark.
        """
        args = create_bookmark_reqparse.parse_args()
        book_id = args["book_id"]
        status = args["status"]
        return process_create_bookmark(book_id, status)


@bookmark_ns.route("/<book_id>", endpoint="bookmark")
class ResourceResource(Resource):
    @bookmark_ns.marshal_with(bookmark_model)
    def get(self, book_id):
        """
        Get  book bookmark.
        """
        return process_get_bookmark(book_id)

    @require_token()
    @bookmark_ns.doc(security="Bearer")
    @bookmark_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookmark_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookmark_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, book_id):
        """
        Delete  book bookmark.
        """
        return process_delete_bookmark(book_id)

    @require_token()
    @bookmark_ns.doc(security="Bearer")
    @bookmark_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookmark_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookmark_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @bookmark_ns.expect(update_bookmark_reqparse)
    def put(self, book_id):
        """
        Update  book bookmark.
        """
        args = update_bookmark_reqparse.parse_args()
        status = args["status"]
        return process_update_bookmark(book_id, status)
