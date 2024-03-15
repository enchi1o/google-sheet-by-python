from flask import make_response
from flask_restx import Resource

# Service
from app.service.auth import AuthService

# DTO
from app.dtos.authDto import authDto

api = authDto.api


@api.route("/", doc=False)
class LoginPage(Resource):
    @api.doc("使用者登入頁面")
    def get(self):
        """
        使用者登入頁面
        """
        return make_response(
            "Hello World <a href='/api/user/login'><button>Login</button></a>"
        )


@api.route("/login")
class UserLogin(Resource):
    @api.doc("使用 Google 帳號登入")
    def get(self):
        """
        使用 Google 帳號登入
        """

        return AuthService.Google.login()


@api.route("/callback", doc=False)
class UserLoginCallback(Resource):
    @api.doc("使用 Google 帳號登入 Callback")
    def get(self):

        return AuthService.Google.callback()
