from flask_restful import reqparse, Resource
from models.salary import SalaryModel
from models.Employee import AuthenticationModel, GradeModel
from models.Designation import DesignationModel
from customeDecorators import Authentication_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from app_init import mail
from flask_mail import Message

HRA = 0.10
DA = 0.25
TA = 0.20


class Salary(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True,
                       help="username required")
    parse.add_argument("month", type=str, required=True, help="Month required")

    @Authentication_required
    def post(self):
        data = Salary.parse.parse_args()
        employee = AuthenticationModel.find_by_username(data['username'])
        if employee:
            basic = GradeModel.query.filter_by(
                emp_id=employee.id).order_by(GradeModel.emp_id.desc()).first().basic
            netamount = basic * HRA + basic * DA + basic * TA + basic
            salary = SalaryModel(data['username'], data['month'], netamount)
            salary.save_to_db()
            # salary get mail
            msg = Message('Salary credited!', recipients=[employee.email])
            msg.body = '''
            Hello  ''' + data['username'].split('.')[0] + ''',
            Your ''' + data['month'] + ''' month salary is credited. You can download salary slip from HRMS portal.\n

            If you have any queries, please feel free to contact the Human Resources  Department. 
            We look forward to your success in the company\n

            Thanks & Regards,
            Name of hr
            HR Executive 
            Direct: +91 6353235503 | W: www.lanetteam.com 
            406, Luxuria Business Hub, Nr. VR Mall, Surat, Gujarat - 395007
            Ground Floor, I.T.P.I Building, Beside Celebration Mall, Bhuwana, Udaipur, Rajasthan - 313001'''
            mail.send(msg)
            return {"Status": "Success"}

        return{"status": "404/Not Found"}


class EmployeeSalaryList(Resource):
    @jwt_required
    def get(self):
        username = AuthenticationModel.find_by_id(get_jwt_identity()).username
        salary = [salary.json() for salary in SalaryModel.query.filter(
            SalaryModel.username == username)]
        return {"salary": salary}


class SalaryDetails(Resource):
    @Authentication_required
    def get(self):
        salary = [salary.json() for salary in SalaryModel.query.all()]
        return {"SalaryDetails": salary}
