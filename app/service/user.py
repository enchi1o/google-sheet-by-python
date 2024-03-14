from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from google.oauth2 import id_token
from google.auth.transport import requests


class AuthService:
    pass
