from flask_sqlalchemy import SQLAlchemy
from app.common.extentions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_salt = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return (
            "<User(email='%s', password_salt='%s', password_hash='%s', active='%s', admin='%s', name='%s')>"
            % (
                self.email,
                self.password_salt,
                self.password_hash,
                self.active,
                self.admin,
                self.name,
            )
        )
