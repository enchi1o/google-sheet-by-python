from flask import Flask

from app.common.extentions import db, migrate, jwt
from app.config.config import config
from app.routes import api


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    return app
