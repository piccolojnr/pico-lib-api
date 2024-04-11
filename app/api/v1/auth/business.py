from http import HTTPStatus
from flask import jsonify, current_app, url_for
import jwt
from app import db, mail, auth_manager
from flask_restx import abort
from app.models import User, Profile, UserGender
from flask_pyjwt import current_token
from flask_mail import Message


def process_registeration_reguest(email, password, first_name, last_name, gender):
    if User.find_by_email(email):
        abort(HTTPStatus.BAD_REQUEST, "User already exists")

    new_user: User = User(email=email, password=password)
    db.session.add(new_user)
    db.session.flush()

    new_profile: Profile = Profile(
        user_id=new_user.id,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        gender=UserGender._value2member_map_[gender],
    )
    db.session.add(new_profile)
    db.session.commit()

    auth = new_user.encode_auth_token()
    response = jsonify(
        status="success",
        message="User registered successfully",
        auth=auth,
        token_type="Bearer",
        expires_in=_get_token_expire_time(),
    )
    response.status_code = HTTPStatus.CREATED
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    # process_send_confirmation_email(new_user.email, new_user.public_id)
    return response


def process_login_request(email, password):
    if not email:
        abort(HTTPStatus.BAD_REQUEST, "Email is required")
    if not password:
        abort(HTTPStatus.BAD_REQUEST, "Password is required")

    user: User = User.find_by_email(email)
    if user and user.check_password(password):
        auth = user.encode_auth_token()
        response = jsonify(
            status="success",
            message="Logged in successfully",
            auth=auth,
            token_type="Bearer",
            expires_in=_get_token_expire_time(),
        )
        response.status_code = HTTPStatus.OK
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        return response
    else:
        abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
        return None


def process_logout_request():
    public_id = current_token.sub["public_id"]
    user: User = User.find_by_public_id(public_id)
    if user:
        res = user.blacklist_token(current_token)
        if res["success"]:
            return jsonify({"message": "Logged out successfully"})
        else:
            abort(HTTPStatus.BAD_REQUEST, "Invalid token")
            return None
    else:
        abort(HTTPStatus.UNAUTHORIZED, "User not found")
        return None
        

def process_refresh_token_request():
    public_id = current_token.sub
    user: User = User.find_by_public_id(public_id)

    if not user:
        abort(HTTPStatus.UNAUTHORIZED, "User not found")
    auth_token = user.generate_auth_token().signed

    return jsonify(message="token refreshed", auth_token=auth_token)


def process_change_password(old_password, new_password, token=None):
    if token:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms="HS256"
        )
        email = payload["email"]
        user: User = User.find_by_email(email)
    else:
        user: User = User.find_by_public_id(current_token.sub["public_id"])

    if not user:
        abort(HTTPStatus.UNAUTHORIZED, "User not found")

    if not token and not user.check_password(old_password):
        abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials")

    user.password = new_password
    db.session.commit()
    return jsonify(message="Password changed successfully")


def process_confirm_email(token, email, password):
    try:
        user: User = User.find_by_email(email)
        if user and user.check_password(password):
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256"
            )
            email = payload["email"]
            user = User.find_by_email(email)
            if user:
                user.is_email_confirmed = True
                db.session.commit()
                return jsonify(message="Email confirmed successfully", status="success")
            else:
                abort(HTTPStatus.UNAUTHORIZED, "User not found")
        else:
            abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
            return None

    except jwt.ExpiredSignatureError:
        abort(HTTPStatus.UNAUTHORIZED, "Token expired")
    except jwt.InvalidTokenError:
        abort(HTTPStatus.UNAUTHORIZED, "Invalid token")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


def _get_token_expire_time():
    token_age_h = current_app.config["TOKEN_EXPIRE_HOURS"]
    token_age_m = current_app.config["TOKEN_EXPIRE_MINUTES"]
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds


def process_send_forgot_password_email(email, public_id):
    try:
        token = _generate_confirmation_token(email, public_id)
        update_password_url = url_for(
            "site.forgot_password", token=token, _external=True
        )
        msg = Message("Forgot Password", recipients=[email])
        msg.body = f"Hello!\n\nWe received a request to reset your password. If this was you, please click on the following link to reset your password:\n\n{update_password_url}\n\nIf you didn't request a password reset, you can safely ignore this email.\n\nBest regards,\nThe Pico-Library Team"
        msg.sender = current_app.config["MAIL_USERNAME"]
        mail.send(msg)
    except Exception as e:
        print(e)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, "Failed to send email")


def process_send_confirmation_email(email, public_id):
    try:
        token = _generate_confirmation_token(email, public_id)
        confirm_email_url = url_for("site.confirm_email", token=token, _external=True)
        msg = Message("Confirm Your Email Address", recipients=[email])
        msg.body = f"Hello!\n\nThank you for registering with us. Please click on the following link to confirm your email address:\n\n{confirm_email_url}\n\nIf you didn't sign up for an account, you can safely ignore this email.\n\nBest regards,\nThe Pico-Library Team"
        msg.sender = current_app.config["MAIL_USERNAME"]
        mail.send(msg)
    except Exception as e:
        print(e)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, "Failed to send email")


def _generate_confirmation_token(email, public_id):
    payload = {
        "email": email,
        "public_id": public_id,
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token
