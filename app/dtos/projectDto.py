from flask_restx import Namespace, fields


class ProjectDto:
    api = Namespace("project", description="專案相關")

    project_post_args = api.model(
        "ProjectPostArgs",
        {
            "project_name": fields.String(
                required=True,
                description="專案名稱",
            ),
            "project_folder_path": fields.String(
                required=True,
                description="Google Drive 資料夾路徑",
            ),
            "description": fields.String(
                required=False,
                description="專案描述",
            ),
        },
    )

    project_delete_args = api.model(
        "ProjectDeleteArgs",
        {
            "project_id": fields.Integer(
                required=True,
                description="專案 ID",
            ),
        },
    )

    project_update_args = api.model(
        "ProjectUpdateArgs",
        {
            "project_id": fields.Integer(
                required=True,
                description="專案 ID",
            ),
            "project_name": fields.String(
                required=True,
                description="專案名稱",
            ),
            "project_folder_path": fields.String(
                required=True,
                description="Google Drive 資料夾路徑",
            ),
            "description": fields.String(
                required=True,
                description="專案描述",
            ),
        },
    )
