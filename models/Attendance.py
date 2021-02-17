from config import db


class AttendanceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    starttime = db.Column(db.String(10), nullable=False)
    endtime = db.Column(db.String(10), default=None)
    date = db.Column(db.String(10), nullable=False)

    def __init__(self, emp_id, starttime, date):
        self.emp_id = emp_id
        self.starttime = starttime
        self.date = date

    @classmethod
    def find_by_id(cls, id):
        return AttendanceModel.query.filter_by(emp_id=id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
