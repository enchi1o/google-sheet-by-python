import os
from hashlib import pbkdf2_hmac


def generate_salt():
    salt = os.urandom(16)
    return salt.hex()


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False


def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()


def validate_user(email, password, user_data):
    try:
        if email == user_data.email:
            saved_password_hash = user_data.password_hash
            saved_password_salt = user_data.password_salt
            password_hash = generate_hash(password, saved_password_salt)

        if password_hash == saved_password_hash:
            user_info = user_data.email
            return user_info
        else:
            return "密碼錯誤，驗證失敗"
    except Exception as e:
        return "讀取 DB 資料錯誤"
