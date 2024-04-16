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

# Create a namespace for authentication
auth_ns = Namespace(name="auth", validate=True)


# Define endpoints for authentication
@auth_ns.route("/", endpoint="auth_user")
class AuthUser(Resource):
    # Endpoint for logging in a user
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


# Define endpoints for authentication
@auth_ns.route("/register", endpoint="auth_register")
class RegisterUser(Resource):
    # Endpoint for registering a new user
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


# Define endpoints for authentication
@auth_ns.route("/login", endpoint="auth_login")
class LoginUser(Resource):
    # Endpoint for logging in a user
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


# Define endpoints for authentication
@auth_ns.route("/refresh", endpoint="auth_refresh")
class RefreshToken(Resource):
    # Endpoint for refreshing a token
    @require_token(token_type="refresh")
    @auth_ns.response(HTTPStatus.OK, "Token refreshed successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Refresh a token")
    @auth_ns.doc(security="Bearer")
    def post(self):
        return process_refresh_token_request()


# Define endpoints for authentication
@auth_ns.route("/logout", endpoint="auth_logout")
class LogoutUser(Resource):
    @require_token()
    @auth_ns.response(HTTPStatus.OK, "User logged out successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Logout a user")
    @auth_ns.doc(security="Bearer")
    def post(self):
        return process_logout_request()


# Define endpoints for authentication
@auth_ns.route("/forgot-password", endpoint="auth_forgot_password")
class ForgotPassword(Resource):
    # Endpoint for sending a forgot password email
    @auth_ns.expect(auth_send_forgot_password_reqparser)
    @auth_ns.response(HTTPStatus.OK, "Email sent successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.doc(description="Send a forgot password email")
    def post(self):
        request_data = auth_send_forgot_password_reqparser.parse_args()
        email = request_data["email"]
        from app.models import User

        user: User = User.query.filter_by(email=email).first()
        if user is None:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        if not user.is_email_confirmed:
            return {"message": "Email not confirmed"}, HTTPStatus.BAD_REQUEST

        return process_send_forgot_password_email(email, user.public_id)


# Define endpoints for authentication
@auth_ns.route("/change-password/<token>", endpoint="auth_change_password_with_token")
class ChangePassword(Resource):
    # Endpoint for changing a user's password
    @auth_ns.expect(auth_change_password_reqparser)
    @auth_ns.response(HTTPStatus.OK, "Password changed successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Change a user's password")
    @auth_ns.doc(security="Bearer")
    def put(self, token):
        request_data = auth_change_password_reqparser.parse_args()
        old_password = request_data["old_password"]
        new_password = request_data["new_password"]
        return process_change_password(old_password, new_password, token)


# Define endpoints for authentication
@auth_ns.route("/change-password", endpoint="auth_change_password")
class ChangePassword(Resource):
    # Endpoint for changing a user's password
    @require_token()
    @auth_ns.expect(auth_change_password_reqparser)
    @auth_ns.response(HTTPStatus.OK, "Password changed successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(description="Change a user's password")
    @auth_ns.doc(security="Bearer")
    def put(self):
        request_data = auth_change_password_reqparser.parse_args()
        old_password = request_data["old_password"]
        new_password = request_data["new_password"]
        return process_change_password(old_password, new_password, None)


# Define endpoints for authentication
@auth_ns.route("/protected_route", endpoint="protected_route")
class ProtectedRoute(Resource):
    # Endpoint for a protected route
    @require_token()
    def get(self):
        return {"message": "You've reached the protected route!"}, 200


# Define endpoints for authentication
@auth_ns.route("/admin_protected_route", endpoint="admin_protected_route")
class ProtectedRoute(Resource):
    # Endpoint for a protected route
    @require_token(scope={"is_admin": True})
    def get(self):
        return {"message": "You've reached the admin protected route!"}, 200


# Define endpoints for authentication
@auth_ns.route("/confirm-email/<token>", endpoint="confirm_email")
class ConfirmEmail(Resource):
    # Endpoint for confirming an email
    @auth_ns.expect(auth_login_reqparser)
    def post(self, token):
        request_data = auth_login_reqparser.parse_args()
        email = request_data["email"]
        password = request_data["password"]
        return process_confirm_email(token, email, password)


# Define endpoints for authentication
@auth_ns.route("/confirm-email", endpoint="send_confirm_email")
class SendConfirmationEmail(Resource):
    # Endpoint for sending a confirmation email
    @require_token()
    @auth_ns.response(HTTPStatus.OK, "Email sent successfully")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Bad request")
    @auth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.NOT_FOUND, "Not found")
    @auth_ns.doc(security="Bearer")
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
