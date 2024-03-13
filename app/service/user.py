from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_OAUTH2_CLIENT_ID = ""


class AuthService:
    @staticmethod
    def google_login(token: str) -> str:
        try:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_OAUTH2_CLIENT_ID
            )
            if id_info["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise ValueError("Wrong issuer.")
        except ValueError:
            # Invalid token
            raise ValueError("Invalid token")

        return "登入成功", 200
