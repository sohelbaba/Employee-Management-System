from config import db
import datetime
from sqlalchemy import DateTime
from models.Employee import AuthenticationModel


class TaskModel(db.Model):

    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey("authentication.id"))
    desc = db.Column(db.Text, nullable=False)
    technology = db.Column(db.String(50), nullable=False)
    projectname = db.Column(db.String(50), nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, emp_id, technology, projectname, hour, desc):
        self.emp_id = emp_id
        self.technology = technology
        self.projectname = projectname
        self.hour = hour
        self.desc = desc

    def json(self):
        return {
            "id": self.id,
            "Username": AuthenticationModel.find_by_id(self.emp_id).username,
            "Technology": self.technology,
            "ProjectName": self.projectname,
            "hour": self.hour,
            "desc": self.desc,
            "DateTime": str(self.date).split(".")[0],
        }

    @classmethod
    def find_by_id(cls, taskid):
        return TaskModel.query.filter_by(id=taskid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
