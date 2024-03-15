from flask_restx import Api

api = Api(
    title="TestCenter API",
    version="v1",
    openapi_version="3.0.0",
    description="Using GoogleSheet and GoogleDrive to manage test center data.",
    doc="/api/doc",
    prefix="/api",
    authorizations={
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "請輸入 Bearer $token",
        }
    },
)

from .auth import api as user_ns
from .project import api as project_ns

api.add_namespace(user_ns, path="/user")
api.add_namespace(project_ns, path="/project")
