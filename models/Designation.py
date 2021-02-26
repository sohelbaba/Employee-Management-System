from config import db

# it holds the company designation's detail


class DesignationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(12), nullable=False)
    basic = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, designation, basic):
        self.designation = designation
        self.basic = basic

    @classmethod
    def find_by_designation(cls, designation):
        return DesignationModel.query.filter_by(designation=designation).first()

    def json(self):
        return{
            "Designation": self.designation,
            "Basic": self.basic
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
