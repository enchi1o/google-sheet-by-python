from flask_restx import Resource
from app.decorators.auth import admin_required, basic_required

# Service
from app.service.project import ProjectService

# DTO
from app.dtos.projectDto import ProjectDto

api = ProjectDto.api


@api.route("")
class WorkflowProject(Resource):
    @api.doc(description="新增專案", security="Bearer Auth")
    @api.expect(ProjectDto.project_post_args, validate=True)
    @api.response(
        code=200,
        description="新增專案成功",
    )
    @admin_required
    def post(self):
        # 新增專案 Service
        return ProjectService.insert(
            project_name=api.payload["project_name"],
            project_folder_path=api.payload["project_folder_path"],
            description=api.payload["description"],
        )

    @api.doc(description="查詢所有專案", security="Bearer Auth")
    @api.response(
        code=200,
        description="查詢所有專案成功",
    )
    @basic_required
    def get(self):
        # 查詢所有專案 Service
        return ProjectService.query_all()

    @api.doc(description="更新專案", security="Bearer Auth")
    @api.expect(ProjectDto.project_update_args, validate=True)
    @admin_required
    def put(self):
        # 更新專案 Service
        return ProjectService.update_by_project_id(
            project_id=api.payload["project_id"],
            project_name=api.payload["project_name"],
            webhook_url=api.payload["webhook_url"],
        )

    @api.doc(description="刪除專案", security="Bearer Auth")
    @api.expect(ProjectDto.project_delete_args, validate=True)
    @admin_required
    def delete(self):
        # 刪除專案 Service
        return ProjectService.delete_by_project_id(project_id=api.payload["project_id"])
