from flask_restx import Resource

# Service
from app.service.user import AuthService

# DTO
from app.dtos.userDto import userDto

api = userDto.api


@api.route("/login")
class UserLogin(Resource):
    @api.doc("使用者登入")
    @api.expect(userDto.google_args, validate=True)
    @api.marshal_with(userDto.response_model)
    def post(self):
        """
        使用者登入
        """

        token = api.payload["token"]
        return AuthService.google_login(token)
