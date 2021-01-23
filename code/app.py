from flask import Flask
from flask_restful import Api
from resources.Employees import (
    EmployeeRegister, EmployeeLogin, EmployeePersonalDetails, Employee, EmployeeQualificationDetails,
    EmployeeAddressDetails, EmployeeSalaryDetails)
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = 'EmployeeManagementSystem'

api = Api(app)
jwt = JWTManager(app)

# set database url
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@app.before_first_request
def init_db():
    db.create_all()


api.add_resource(EmployeeRegister, '/employee/register',
                 '/employee/<string:username>')
api.add_resource(EmployeeLogin, '/employee/login')
api.add_resource(Employee, '/employee/details')
api.add_resource(EmployeePersonalDetails, '/employee/profile')
api.add_resource(EmployeeAddressDetails, '/employee/address')
api.add_resource(EmployeeQualificationDetails, '/employee/qualification')
api.add_resource(EmployeeSalaryDetails, '/employee/salaryinfo')


if __name__ == '__main__':
    from config import db
    db.init_app(app)
    app.run(port=5000, debug=True)
