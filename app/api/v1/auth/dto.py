from flask_restx.reqparse import RequestParser
from flask_restx.inputs import email
from flask_restx.model import Model
from flask_restx.fields import String, Boolean


# DTOs
# data model for user
user_model = Model(
    "User",
    {
        "email": String,
        "is_admin": Boolean,
        "is_email_confirmed": Boolean,
        "public_id": String,
    },
)


# parsers
auth_register_reqparser = RequestParser(bundle_errors=True)
auth_register_reqparser.add_argument(
    "password",
    type=str,
    required=True,
    location="form",
    help="Password required" "email",
)
auth_register_reqparser.add_argument(
    "email",
    type=email(),
    required=True,
    location="form",
    help="Email required" "first_name",
)
auth_register_reqparser.add_argument(
    "first_name",
    type=str,
    required=True,
    location="form",
    help="First name required" "last_name",
)
auth_register_reqparser.add_argument(
    "last_name",
    type=str,
    required=True,
    location="form",
    help="Last name required",
)
auth_register_reqparser.add_argument(
    "gender",
    type=str,
    choices=["male", "female", "other"],
    required=True,
    location="form",
    help="Gender required",
)


# parsers
auth_login_reqparser = RequestParser(bundle_errors=True)
auth_login_reqparser.add_argument(
    "password",
    type=str,
    required=True,
    location="form",
    help="Password required",
)
auth_login_reqparser.add_argument(
    "email",
    type=email(),
    required=True,
    location="form",
    help="Email required",
)

# parsers
auth_change_password_reqparser = RequestParser(bundle_errors=True)
auth_change_password_reqparser.add_argument(
    "old_password",
    type=str,
    required=False,
    location="form",
)
auth_change_password_reqparser.add_argument(
    "token",
    type=str,
    required=False,
    location="form",
)
auth_change_password_reqparser.add_argument(
    "new_password",
    type=str,
    required=False,
    location="form",
    help="New password required",
)
auth_send_forgot_password_reqparser = RequestParser(bundle_errors=True)
auth_send_forgot_password_reqparser.add_argument(
    "email",
    type=email(),
    required=True,
    location="form",
    help="Email required",
)
