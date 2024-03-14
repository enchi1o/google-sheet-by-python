import os
import pathlib
from functools import wraps

from flask import (
    make_response,
    session,
    redirect,
    request,
)
from flask_restx import Resource
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import requests
from pip._vendor import cachecontrol
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# DTO
from app.dtos.userDto import userDto


api = userDto.api
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "..\..\client_secret.json"
)
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://localhost:8080/api/user/callback",
)


def login_is_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return "權限問題", 401  # Authorization required
        else:
            return fn(*args, **kwargs)

    return wrapper


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
        authorization_url, state = flow.authorization_url()
        print(authorization_url)
        session["state"] = state
        return redirect(authorization_url)


@api.route("/callback", doc=False)
class UserLoginCallback(Resource):
    @api.doc("使用者登入Callback")
    def get(self):
        if "http:" in request.url:
            request.url = request.url.replace("http:", "https:", 1)
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            return "錯誤", 500  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID,
        )

        print(id_info.get("sub"), id_info.get("name"), id_info.get("email"))
        print(id_info)
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["email"] = id_info.get("email")
        return id_info, 200


@api.route("/protected_area")
class ProtectedArea(Resource):
    @api.doc("保護區")
    @login_is_required
    def get(self):
        return make_response(
            f"Hello {session['name']}-{session['email']} <a href='/api/user/logout'><button>Logout</button></a>"
        )
