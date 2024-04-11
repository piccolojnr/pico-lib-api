from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from http import HTTPStatus
from .dto import (
    create_subject_parser,
    pagination_links_model,
    pagination_reqparse,
    subject_model,
    subject_pagination_model,
    user_subject_model,
    update_subject_parser,
)
from .business import (
    process_create_subject,
    process_create_subject_book,
    process_create_subject_user,
    process_delete_subject,
    process_delete_subject_book,
    process_delete_subject_user,
    process_get_subject,
    process_get_subjects,
    process_update_subject,
)

subjects_ns = Namespace(name="subjects", validate=True)
subjects_ns.models[subject_model.name] = subject_model
subjects_ns.models[subject_pagination_model.name] = subject_pagination_model
subjects_ns.models[pagination_links_model.name] = pagination_links_model
subjects_ns.models[user_subject_model.name] = user_subject_model


@subjects_ns.route("/", endpoint="subjects")
class SubjectsResource(Resource):
    @subjects_ns.expect(pagination_reqparse)
    def get(self):
        """
        Get subjects.
        """
        args = pagination_reqparse.parse_args()
        page = args["page"]
        per_page = args["per_page"]
        q = args["q"]
        return process_get_subjects(page, per_page, q)

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @subjects_ns.expect(create_subject_parser)
    def post(self):
        """
        Create subject.
        """
        args = create_subject_parser.parse_args()
        name = args["name"]
        return process_create_subject(name)


@subjects_ns.route("/<subject_id>", endpoint="subject")
class SubjectResource(Resource):
    @subjects_ns.marshal_with(subject_model)
    def get(self, subject_id):
        """
        Get subject.
        """
        return process_get_subject(subject_id)

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, subject_id):
        """
        Delete subject.
        """
        return process_delete_subject(subject_id)

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @subjects_ns.expect(update_subject_parser, validate=True)
    def put(self, subject_id):
        """
        Update subject.
        """
        args = update_subject_parser.parse_args()
        name = args["name"]
        score = args["score"]
        return process_update_subject(subject_id, name, score)


@subjects_ns.route("/<subject_id>/books/<book_id>", endpoint="subject_book")
class SubjectBookResource(Resource):
    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, subject_id, book_id):
        """
        Delete subject's book.
        """
        return process_delete_subject_book(subject_id, book_id)

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, subject_id, book_id):
        """
        Create subject's book.
        """
        return process_create_subject_book(subject_id, book_id)


@subjects_ns.route("/<subject_id>/users/<user_public_id>", endpoint="subject_user")
class SubjectUsersResource(Resource):
    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self, subject_id, user_public_id):
        """
        Delete subject's user.
        """
        return process_delete_subject_user(subject_id, user_public_id)

    @require_token()
    @subjects_ns.doc(security="Bearer")
    @subjects_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @subjects_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @subjects_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def post(self, subject_id, user_public_id):
        """
        Create subject's user.
        """
        return process_create_subject_user(subject_id, user_public_id)
