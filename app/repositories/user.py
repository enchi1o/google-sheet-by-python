from app import db
from app.model.user_model import User

# Sqlalchemy Error
from sqlalchemy.exc import SQLAlchemyError


def respModel(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "active": user.active,
        "admin": user.admin,
    }


class User:
    @staticmethod
    def db_register_insert(email, password_salt, password_hash, user_name):
        try:
            user = User(
                email=email,
                password_salt=password_salt,
                password_hash=password_hash,
                name=user_name,
            )
            db.session.add(user)
            db.session.commit()

            result = {"status": 1, "msg": "註冊成功"}
            return result
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            result = {"status": 0, "msg": error}
            return result

    @staticmethod
    def db_query_by_email(email):
        try:
            user = User.query.filter_by(email=email).first()
            result = {"status": 1, "msg": "查詢成功", "data": user}
            return result
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            result = {"status": 0, "msg": error}
            return result

    @staticmethod
    def db_query_all():
        try:
            users = User.query.all()
            users_list = []
            for user in users:
                user_dict = respModel(user)
                users_list.append(user_dict)

            result = {"status": 1, "msg": "查詢成功", "data": users_list}
            return result
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            result = {"status": 0, "msg": error}
            return result
