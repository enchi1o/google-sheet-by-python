from functools import wraps

from flask import abort
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidSignatureError
from werkzeug.exceptions import HTTPException

from app.repositories.user import Auth


def get_user_system_permission():
    """
    取得使用者的系統權限

    Return:
        - admin / basic
    """
    try:
        verify_jwt_in_request()
        sub = get_jwt_identity()
        info = Auth.db_query_by_email(email=sub)

        if not info["data"].active:
            abort(403, "該使用者 active 未開啟，請聯絡管理者開啟")

        is_admin = info["data"].admin

        return "admin" if bool(is_admin) else "basic"

    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code, e.description)

        elif isinstance(e, ExpiredSignatureError):
            abort(401, "Token 已過期，請重新登入")

        elif isinstance(e, DecodeError) or isinstance(e, InvalidSignatureError):
            abort(401, "Token 無效，請重新登入")

        else:
            abort(403, "非系統使用者")


def admin_required(fn):
    """
    檢查使用者是否為 Admin
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            system_permission = get_user_system_permission()

            if system_permission != "admin":
                abort(403, "權限不足")

            return fn(*args, **kwargs)

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code, e.description)

    return wrapper


def basic_required(fn):
    """
    檢查使否為系統使用者
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            system_permission = get_user_system_permission()

            if system_permission not in ["admin", "basic"]:
                abort(403, "權限不足")

            return fn(*args, **kwargs)

        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code, e.description)

    return wrapper
