from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask_pyjwt import require_token
from app.models import BlacklistedToken

token_ns = Namespace(name="tokens", validate=True)


@token_ns.route("/", endpoint="clear_tokens")
class ProfileRoute(Resource):

    @require_token(scope={"is_admin": True})
    @token_ns.doc(security="Bearer")
    @token_ns.response(int(HTTPStatus.OK), "Token is currently valid.")
    @token_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @token_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    def delete(self):
        """
        Clear all tokens from the database.
        """
        BlacklistedToken.delete_expired()
        return {"status": "success", "message": "Tokens cleared successfully."}
