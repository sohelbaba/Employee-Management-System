from config import db
import datetime
from sqlalchemy import DateTime


class TaskModel(db.Model):

    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    task = db.Column(db.Text, nullable=False)
    task_log = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, emp_id, task, task_log):
        self.emp_id = emp_id
        self.task = task
        self.task_log = task_log

    def json(self):
        return{
            "Task": self.task,
            "Log": self.task_log,
            "DateTime": str(self.date).split('.')[0]
        }

    @classmethod
    def find_by_id(cls, taskid):
        return TaskModel.query.filter_by(id=taskid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
