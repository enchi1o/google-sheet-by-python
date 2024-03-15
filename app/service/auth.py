import os
import pathlib
import requests

from pip._vendor import cachecontrol
from dotenv import load_dotenv

from flask import (
    session,
    redirect,
    request,
)

from flask_jwt_extended import create_access_token

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from app.utils.auth import (
    generate_hash,
    generate_salt,
)

from app.repositories.user import UserRepo

load_dotenv(dotenv_path=".env")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class AuthService:
    class Google:

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

        @staticmethod
        def login():
            authorization_url, state = AuthService.Google.flow.authorization_url()

            return redirect(authorization_url)

        @staticmethod
        def callback():
            if "http:" in request.url:
                request.url = request.url.replace("http:", "https:", 1)
            AuthService.Google.flow.fetch_token(authorization_response=request.url)

            credentials = AuthService.Google.flow.credentials
            request_session = requests.session()
            cached_session = cachecontrol.CacheControl(request_session)
            token_request = google.auth.transport.requests.Request(
                session=cached_session
            )

            id_info = id_token.verify_oauth2_token(
                id_token=credentials._id_token,
                request=token_request,
                audience=GOOGLE_CLIENT_ID,
            )

            user = UserRepo.db_query_by_email(id_info["email"])

            if user["status"] == 0:
                return "資料庫異常", 500
            elif user["data"] != [] and user["data"] != None:
                access_token = create_access_token(identity=id_info["email"])
                return {
                    "status": 1,
                    "retMsg": "登入成功",
                    "access_token": access_token,
                }, 200
            else:
                regist = AuthService.Google.register(
                    user_email=id_info["email"],
                    user_password=id_info["sub"],
                    user_name=id_info["name"],
                )
                if regist["status"] == 1:
                    access_token = create_access_token(identity=id_info["email"])
                    return {
                        "status": 1,
                        "retMsg": "登入成功",
                        "access_token": access_token,
                    }, 200
                else:
                    return {
                        "status": 0,
                        "retMsg": regist["retMsg"],
                        "retCode": 500,
                    }, 500

        @staticmethod
        def register(user_email: str, user_password: str, user_name: str):
            password_salt = generate_salt()
            password_hash = generate_hash(user_password, password_salt)
            user_insert_info = UserRepo.db_register_insert(
                user_email, password_salt, password_hash, user_name
            )
            if user_insert_info["status"] == 1:
                retVal = {"status": 1, "retMsg": "註冊成功"}
                return retVal
            else:
                """未註冊成功，走以下流程"""
                retVal = {
                    "status": 0,
                    "retMsg": user_insert_info["error"],
                    "retCode": 500,
                }
                return retVal
