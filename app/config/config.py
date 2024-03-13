import os
import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
basedir = os.path.abspath(os.path.dirname(__file__))

DB_HOST = os.environ.get("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
DB_PORT = os.environ.get("DB_PORT")
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")


class BaseConfig:  # 基本配置
    SECRET_KEY = os.urandom(24)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=14)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=8)


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    )
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = JWT_SECRET_KEY


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True
    JWT_SECRET_KEY = JWT_SECRET_KEY


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
