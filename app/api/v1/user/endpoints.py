from flask_restx import Namespace, Resource
from flask import request
from flask_pyjwt import require_token
from app.api.v1.user.business import (
    process_user_profile_request,
    process_user_profile_update,
)
from http import HTTPStatus
from app.api.v1.user.dto import short_profile_model, user_model, profile_model

user_ns = Namespace(name="user", validate=True)
user_ns.models[user_model.name] = user_model
user_ns.models[profile_model.name] = profile_model
user_ns.models[short_profile_model.name] = short_profile_model


@user_ns.route("/profile", endpoint="user_profile")
class ProfileRoute(Resource):

    @require_token()
    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.", profile_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @user_ns.marshal_with(profile_model)
    def get(self):
        return process_user_profile_request()

    @require_token()
    @user_ns.doc(security="Bearer")
    @user_ns.expect(profile_model)
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.", profile_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def put(self):
        profile_dict = request.get_json()
        return process_user_profile_update(profile_dict)
