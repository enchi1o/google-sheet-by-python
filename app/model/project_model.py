from app.common.extentions import db


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    folder_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
