from app import db
from app.model.project_model import Project

# Sqlalchemy Error
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


def respModel(project):
    return {
        "id": project.id,
        "name": project.name,
        "folder_path": project.folder_path,
    }


class ProjectRepo:
    @staticmethod
    def db_insert(project_name, folder_path, description):
        try:
            search_project = Project.query.filter_by(project_name=project_name).first()
            if search_project is not None:
                return {"status": 0, "msg": "專案已存在"}

            project = Project(
                project_name=project_name,
                folder_path=folder_path,
                description=description,
            )
            db.session.add(project)
            db.session.commit()
            project_msg = respModel(project)

            return {"status": 1, "msg": "寫入成功", "data": project_msg}
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return {"status": 0, "msg": error}

    @staticmethod
    def db_update_by_project_id(project_id, project_name, folder_path, description):
        try:
            project = Project.query.filter_by(id=project_id).first()
            if project is None:
                return {"status": 0, "msg": "專案不存在"}

            project.project_name = project_name
            project.folder_path = folder_path
            project.description = description
            db.session.commit()
            project_dict = respModel(project)

            return {"status": 1, "msg": "更新成功", "data": project_dict}
        except IntegrityError as e:
            error = str(e.__dict__["orig"])
            if "Duplicate entry" in error:
                return {"status": 0, "msg": "專案名稱重複"}
            return {"status": 0, "msg": error}
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return {"status": 0, "msg": error}

    @staticmethod
    def db_query_all():
        try:
            projects = Project.query.all()
            projects_list = [respModel(project) for project in projects]

            return {"status": 1, "msg": "查詢成功", "data": projects_list}
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return {"status": 0, "msg": error}

    @staticmethod
    def db_delete_by_project_id(project_id):
        try:
            project = Project.query.filter_by(id=project_id).first()
            if project is None:
                return {"status": 0, "msg": "專案不存在"}
            db.session.delete(project)
            db.session.commit()
            project_msg = respModel(project)

            return {"status": 1, "msg": "刪除成功", "data": project_msg}
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return {"status": 0, "msg": error}

    @staticmethod
    def db_query_by_project_name(project_name):
        try:
            project = Project.query.filter_by(project_name=project_name).first()
            if project is None:
                return {"status": 0, "msg": "專案不存在"}
            project_msg = respModel(project)

            return {"status": 1, "msg": "查詢成功", "data": project_msg}
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return {"status": 0, "msg": error}
