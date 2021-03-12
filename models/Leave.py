from config import db
import datetime
from sqlalchemy import DateTime
from models.Employee import AuthenticationModel


class LeaveModel(db.Model):
    __tablename__ = "leave"
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey("authentication.id"))
    senction_by_id = db.Column(db.Integer, default=None)
    leave_type = db.Column(db.String(5), nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)
    apply_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    senction_date = db.Column(db.DateTime, default=None)
    status = db.Column(db.String(10), default="Pending")
    leave_Description = db.Column(db.Text, nullable=False)

    def __init__(self, emp_id, leave_type, start_date, end_date, leave_Description, status=None):
        self.emp_id = emp_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.leave_Description = leave_Description
        self.status = status

    def json(self):
        return {
            "Start Date": str(self.start_date),
            "End Date": str(self.end_date),
            "Type": self.leave_type,
            "Apply Date": str(self.apply_date),
            "Status": self.status,
            "id": self.emp_id,
            "leave_id": self.id,
            "Username": AuthenticationModel.find_by_id(self.emp_id).username,
            "Description": self.leave_Description,
        }

    @classmethod
    def find_by_id(cls, id):
        return LeaveModel.query.filter_by(emp_id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
