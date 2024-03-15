from app.repositories.project import ProjectRepo

from app.utils.ResponseModel import RespModel


class ProjectService:
    @staticmethod
    def insert(project_name, folder_path, description):

        info = ProjectRepo.db_insert(project_name, folder_path, description)
        if info["status"] == 0:
            return RespModel(retMsg=info["msg"], retCode=400).result()
        else:
            return RespModel(retMsg="新增成功", retVal=info["data"]).result()

    @staticmethod
    def query_all():

        info = ProjectRepo.db_query_all()
        if info["status"] == 0:
            return RespModel(retMsg=info["msg"], retCode=400).result()
        else:
            return RespModel(
                retMsg="查詢成功", retVal=info["data"], retCode=200
            ).result()

    @staticmethod
    def delete_by_project_id(project_id):

        info = ProjectRepo.db_delete_by_project_id(project_id)
        if info["status"] == 0:
            return RespModel(retMsg=info["msg"], retCode=400).result()
        else:
            return RespModel(retMsg="刪除成功", retVal=info["data"]).result()

    @staticmethod
    def update_by_project_id(project_id, project_name, folder_path, description):

        info = ProjectRepo.db_update_by_project_id(
            project_id, project_name, folder_path, description
        )
        if info["status"] == 0:
            return RespModel(retMsg=info["msg"], retCode=400).result()
        else:
            return RespModel(retMsg="更新成功", retVal=info["data"]).result()
