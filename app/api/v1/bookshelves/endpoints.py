from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from flask import request
from http import HTTPStatus
from .business import (
    process_create_bookshelf,
    process_delete_bookshelf,
    process_get_bookshelf,
    process_get_bookshelves,
    process_get_bookshelves_by_user,
    process_update_bookshelf,
    process_create_bookshelf_book_relationship,
    process_delete_bookshelf_book_relationship,
)
from .dto import (
    create_bookshelf_model,
    update_bookshelf_model,
    bookshelf_pagination_model,
    bookshelf_model,
    pagination_links_model,
    short_bookshelf_model,
    pagination_reqparser,
)

bookshelves_ns = Namespace(name="bookshelves", validate=True)
bookshelves_ns.models[create_bookshelf_model.name] = create_bookshelf_model
bookshelves_ns.models[update_bookshelf_model.name] = update_bookshelf_model
bookshelves_ns.models[bookshelf_pagination_model.name] = bookshelf_pagination_model
bookshelves_ns.models[bookshelf_model.name] = bookshelf_model
bookshelves_ns.models[pagination_links_model.name] = pagination_links_model
bookshelves_ns.models[short_bookshelf_model.name] = short_bookshelf_model


@bookshelves_ns.route("/", endpoint="bookshelves")
class BookshelvesResource(Resource):
    @bookshelves_ns.expect(pagination_reqparser)
    def get(self):
        """
        Get bookshelves.
        """
        args = pagination_reqparser.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        q = args["q"]
        return process_get_bookshelves(page, per_page, q)

    @require_token(scope={"is_admin": True})
    @bookshelves_ns.doc(security="Bearer")
    @bookshelves_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves_ns.response(
        int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired."
    )
    @bookshelves_ns.expect(create_bookshelf_model)
    def post(self):
        """
        Create bookshelf.
        """
        data = request.get_json()
        return process_create_bookshelf(data)


@bookshelves_ns.route("/<bookshelf_id>", endpoint="bookshelf")
class BookshelfResource(Resource):
    def get(self, bookshelf_id):
        """
        Get bookshelf.
        """
        return process_get_bookshelf(bookshelf_id)

    @require_token(scope={"is_admin": True})
    @bookshelves_ns.doc(security="Bearer")
    @bookshelves_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves_ns.response(
        int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired."
    )
    def delete(self, bookshelf_id):
        """
        Delete bookshelf.
        """
        return process_delete_bookshelf(bookshelf_id)

    @require_token(scope={"is_admin": True})
    @bookshelves_ns.doc(security="Bearer")
    @bookshelves_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves_ns.response(
        int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired."
    )
    @bookshelves_ns.expect(update_bookshelf_model)
    def put(self, bookshelf_id):
        """
        Update bookshelf.
        """
        data = request.get_json()
        return process_update_bookshelf(bookshelf_id, data)


@bookshelves_ns.route("<bookshelf_id>/books/<book_id>", endpoint="bookshelf_book")
class BookshelfBookResource(Resource):
    @require_token(scope={"is_admin": True})
    @bookshelves_ns.doc(security="Bearer")
    @bookshelves_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves_ns.response(
        int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired."
    )
    def delete(self, bookshelf_id, book_id):
        """
        Delete bookshelf's book.
        """
        return process_delete_bookshelf_book_relationship(bookshelf_id, book_id)

    @require_token(scope={"is_admin": True})
    @bookshelves_ns.doc(security="Bearer")
    @bookshelves_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @bookshelves_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @bookshelves_ns.response(
        int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired."
    )
    def post(self, bookshelf_id, book_id):
        """
        Add book to bookshelf.
        """
        return process_create_bookshelf_book_relationship(bookshelf_id, book_id)


@bookshelves_ns.route("/<user_id>", endpoint="bookshelves_by_user")
class BookshelvesByUserResource(Resource):
    @bookshelves_ns.expect(pagination_reqparser)
    def get(self, user_id):
        """
        Get bookshelves by user.
        """
        args = pagination_reqparser.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_bookshelves_by_user(user_id, page, per_page)
