from flask_restx import Namespace, Resource, abort
from app.api.v1.auth.business import (
    process_login_request,
    process_registeration_reguest,
    process_refresh_token_request,
    process_logout_request,
    process_change_password,
    process_confirm_email,
    process_send_confirmation_email,
    process_send_forgot_password_email,
)
from flask_pyjwt import require_token, current_token
from http import HTTPStatus
from app.api.v1.auth.dto import (
    auth_register_reqparser,
    auth_login_reqparser,
    auth_change_password_reqparser,
    auth_send_forgot_password_reqparser,
    user_model,
)

auth_ns = Namespace(name="auth", validate=True)


@auth_ns.route("/", endpoint="auth_user")
class AuthUser(Resource):
    @require_token()
    @auth_ns.response(HTTPStatus.OK, "User logged in successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Login a user")
    @auth_ns.doc(security="Bearer")
    @auth_ns.marshal_with(user_model)
    def get(self):
        from app.models import User

        public_id = current_token.sub["public_id"]

        user = User.find_by_public_id(public_id)
        if not user:
            abort(HTTPStatus.NOT_FOUND, "User not found")
        return user


@auth_ns.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    @auth_ns.expect(auth_register_reqparser)
    @auth_ns.response(HTTPStatus.CREATED, "User created successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Register a new user")
    @auth_ns.doc(security="Bearer")
    def post(self):
        request_data = auth_register_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        first_name = request_data["first_name"]
        last_name = request_data["last_name"]
        gender = request_data["gender"]
        return process_registeration_reguest(
            email, password, first_name, last_name, gender
        )


@auth_ns.route("/login", endpoint="auth_login")
class LoginUser(Resource):
    @auth_ns.expect(auth_login_reqparser)
    @auth_ns.response(HTTPStatus.OK, "User logged in successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Login a user")
    @auth_ns.doc(security="Bearer")
    def post(self):
        request_data = auth_login_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        return process_login_request(email, password)


@auth_ns.route("/refresh", endpoint="auth_refresh")
class RefreshToken(Resource):
    @require_token("refresh")
    @auth_ns.response(HTTPStatus.OK, "Token refreshed successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Refresh a token")
    @auth_ns.doc(security="Bearer")
    def post(self):
        return process_refresh_token_request()


@auth_ns.route("/logout", endpoint="auth_logout")
class LogoutUser(Resource):
    @require_token()
    @auth_ns.response(HTTPStatus.OK, "User logged out successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Logout a user")
    @auth_ns.doc(security="Bearer")
    def post(self):
        return process_logout_request()


@auth_ns.route("/forgot_password", endpoint="auth_forgot_password")
class ForgotPassword(Resource):
    @auth_ns.expect(auth_send_forgot_password_reqparser)
    @auth_ns.response(HTTPStatus.OK, "Email sent successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.doc(description="Send a forgot password email")
    def post(self):
        request_data = auth_send_forgot_password_reqparser.parse_args()
        email = request_data["email"]
        from app.models import User

        user = User.query.filter_by(email=email).first()
        if user is None:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        return process_send_forgot_password_email(email, user.public_id)


@auth_ns.route("/change_password", endpoint="auth_change_password")
class ChangePassword(Resource):
    @auth_ns.expect(auth_change_password_reqparser)
    @auth_ns.response(HTTPStatus.OK, "Password changed successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.CONFLICT, "User already exists")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Change a user's password")
    @auth_ns.doc(security="Bearer")
    def put(self):
        request_data = auth_change_password_reqparser.parse_args()
        old_password = request_data["old_password"]
        new_password = request_data["new_password"]
        token = request_data["token"]
        return process_change_password(old_password, new_password, token)


@auth_ns.route("/protected_route", endpoint="protected_route")
class ProtectedRoute(Resource):
    @require_token()
    def get(self):
        return {"message": "You've reached the protected route!"}, 200


@auth_ns.route("/admin_protected_route", endpoint="admin_protected_route")
class ProtectedRoute(Resource):
    @require_token(scope={"is_admin": True})
    def get(self):
        return {"message": "You've reached the admin protected route!"}, 200


@auth_ns.route("/confirm_email/<token>", endpoint="confirm_email")
class ConfirmEmail(Resource):
    @auth_ns.expect(auth_login_reqparser)
    def post(self, token):
        request_data = auth_login_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        return process_confirm_email(token, email, password)


@auth_ns.route("/send_confirmation_email", endpoint="send_confirmation_email")
class SendConfirmationEmail(Resource):
    @require_token()
    def post(self):
        from app.models import User

        from flask import jsonify

        public_id = current_token.sub["public_id"]

        user = User.find_by_public_id(public_id)
        if user is None:
            abort(404, "User not found")
        else:
            process_send_confirmation_email(user.email, user.public_id)
            return jsonify({"message": "Email sent successfully"})
