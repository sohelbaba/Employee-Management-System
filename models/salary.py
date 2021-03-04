from config import db
from sqlalchemy import DateTime
import datetime


class SalaryModel(db.Model):
    __tablename__ = 'salary'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    month = db.Column(db.String(10), nullable=False)
    generateddate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    amount = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, username, month, amount):
        self.username = username
        self.month = month
        self.amount = amount

    def json(self):
        return{
            "username": self.username,
            "month": self.month,
            "generateddate": str(self.generateddate),
            "amount": self.amount
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
