from flask import Flask
from flask_restful import Api


app = Flask(__name__)
app.secret_key = 'EmployeeManagementSystem'

api = Api(app)

# set database url
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.before_first_request
def init_db():
    db.create_all()


if __name__ == '__main__':
    from config import db
    db.init_app(app)
    app.run(port=5000, debug=True)
