from flask_pyjwt import current_token
from app.models import (
    User,
    Profile,
)
from flask_restx import abort, marshal
from http import HTTPStatus
from app.api.v1.user.dto import (
    profile_model,
)
from app import db


def process_user_profile_request():
    public_id = current_token.sub["public_id"]
    user: User = User.find_by_public_id(public_id)
    if user:
        if user.profile:
            return user.profile
        else:
            user.profile = Profile(first_name="john", last_name="doe", user_id=user.id)
            user.profile.save_to_db()
            return user.profile
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")


def process_user_profile_update(profile_dict):
    public_id = current_token.sub["public_id"]
    user: User = User.find_by_public_id(public_id)
    if user:
        profile = Profile.find_by_user_id(user.id)
        if profile:
            for k, v in profile_dict.items():
                if v is not None:
                    if k not in ["created_at", "updated_at", "user"]:
                        if k == "gender":
                            v = v.upper()
                        setattr(profile, k, v)
            db.session.commit()
            message = f"'{public_id}' profile was successfully updated"
            profile_data = marshal(profile, profile_model)
            response_dict = dict(status="success", message=message, item=profile_data)
            return response_dict, HTTPStatus.OK
        else:
            abort(HTTPStatus.NOT_FOUND, "Profile not found")
    else:
        abort(HTTPStatus.NOT_FOUND, "User not found")
