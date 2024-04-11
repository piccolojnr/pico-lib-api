from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from http import HTTPStatus
from .dto import (
    pagination_links_model,
    pagination_reqparse,
    create_language_reqparse,
    languages_pagination_model,
    langauge_model,
    update_language_reqparse,
)
from .business import (
    process_create_language,
    process_delete_language,
    process_get_language,
    process_update_language,
    process_get_languages,
    process_delete_language_book,
    process_create_language_book,
    process_get_language_books,
)

language_ns = Namespace(name="languages", validate=True)
language_ns.models[langauge_model.name] = langauge_model
language_ns.models[languages_pagination_model.name] = languages_pagination_model
language_ns.models[pagination_links_model.name] = pagination_links_model


@language_ns.route("/", endpoint="languages")
class LanguagesResource(Resource):
    @language_ns.expect(pagination_reqparse)
    def get(self):
        """
        Get  books resources.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_languages(page, per_page)

    @require_token(scope={"is_admin": True})
    @language_ns.expect(create_language_reqparse, validate=True)
    @language_ns.doc(security="Bearer")
    @language_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @language_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @language_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self):
        """
        Create  books language.
        """
        args = create_language_reqparse.parse_args()
        code = args["code"]
        name = args["name"]
        return process_create_language(code, name)


@language_ns.route("/<language_id>", endpoint="language")
class ResourceResource(Resource):
    @language_ns.marshal_with(langauge_model)
    def get(self, language_id):
        """
        Get  book language.
        """
        return process_get_language(language_id)

    @require_token(scope={"is_admin": True})
    @language_ns.doc(security="Bearer")
    @language_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @language_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @language_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, language_id):
        """
        Delete  book language.
        """
        return process_delete_language(language_id)

    @require_token(scope={"is_admin": True})
    @language_ns.doc(security="Bearer")
    @language_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @language_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @language_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @language_ns.expect(update_language_reqparse)
    def put(self, language_id):
        """
        Update  book language.
        """
        args = update_language_reqparse.parse_args()
        code = args["code"]
        name = args["name"]
        return process_update_language(language_id, code, name)


@language_ns.route("/<language_id>/books", endpoint="language_books")
class LanguageBooksResource(Resource):
    @language_ns.expect(pagination_reqparse)
    def get(self, language_id):
        """
        Get language's books.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        return process_get_language_books(language_id, page, per_page)


@language_ns.route("/<language_id>/books/<book_id>", endpoint="language_book")
class LanguageBookResource(Resource):
    @require_token(scope={"is_admin": True})
    @language_ns.doc(security="Bearer")
    @language_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @language_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @language_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, language_id, book_id):
        """
        Delete language's book.
        """
        return process_delete_language_book(language_id, book_id)

    @require_token(scope={"is_admin": True})
    @language_ns.doc(security="Bearer")
    @language_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @language_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @language_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, language_id, book_id):
        """
        Create language's book.
        """
        return process_create_language_book(language_id, book_id)
