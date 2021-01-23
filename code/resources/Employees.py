from flask_restful import Resource, reqparse
from models.Employee import (
    AuthenticationModel, PersonalDetailsModel, AddressModel, QualificationModel, EmployeeSalaryDetailsModel)
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


class EmployeeRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True,
                       help='username is required')
    parse.add_argument('password', type=str, required=True,
                       help='password is required')
    parse.add_argument('role', type=str, required=True,
                       help='role is required')

    def post(self):
        data = EmployeeRegister.parse.parse_args()
        employee = AuthenticationModel.find_by_username(data['username'])

        if employee:
            return {
                "AlreadyExistsError": {
                    "status": False,
                    "error": "Username already exists"
                }
            }
        employee = AuthenticationModel(**data)
        employee.save_to_db()

        return {
            "success": True,
            "message": "Employee Registerd",
            "id": employee.id
        }


class EmployeeLogin(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True,
                       help='username is required')
    parse.add_argument('password', type=str, required=True,
                       help='password is required')

    def get(self):
        data = EmployeeLogin.parse.parse_args()
        employee = AuthenticationModel.find_by_username(data['username'])
        if employee and safe_str_cmp(data['password'], employee.password):
            return {
                "access_token": create_access_token(identity=employee.id),
                "success": True
            }
        return {
            "error": "Username or password incorrent",
            "success": False
        }


class EmployeePersonalDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('firstname', type=str, required=True,
                       help='firstname is required')
    parse.add_argument('lastname', type=str, required=True,
                       help='lastname is required')
    parse.add_argument('gender', type=str, required=True,
                       help='gender is required')
    parse.add_argument('dob', type=str, required=True,
                       help='dob is required')
    parse.add_argument('bloodgroup', type=str, required=True,
                       help='bloodgroup is required')
    parse.add_argument('email', type=str, required=True,
                       help='email is required')
    parse.add_argument('contact', type=str, required=True,
                       help='contact is required')
    parse.add_argument('pancard', type=str, required=True,
                       help='pancard no is required')
    parse.add_argument('aadharcard', type=str, required=True,
                       help='aadharcard no is required')

    @jwt_required
    def get(self):
        employee_personal_details = PersonalDetailsModel.find_by_id(
            get_jwt_identity())
        if employee_personal_details:
            return employee_personal_details.json()
        return {
            "error":  "Data not found",
            "success": False
        }

    @jwt_required
    def post(self):
        data = EmployeePersonalDetails.parse.parse_args()
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            personaldetails = PersonalDetailsModel(
                get_jwt_identity(), data['firstname'], data['lastname'], data['gender'], data['dob'], data['bloodgroup'], data['email'], data['contact'], data['pancard'], data['aadharcard'])
            personaldetails.save_to_db()
            return {
                "success": True
            }
        return {
            "NotFoundError": {
                "success":  False,
                "error": "Employee Not Found"
            }
        }

    @jwt_required
    def put(self):
        data = EmployeePersonalDetails.parse.parse_args()
        employee = PersonalDetailsModel.find_by_id(get_jwt_identity())
        if employee:
            employee.update_to_db(data['firstname'], data['lastname'], data['gender'], data['dob'],
                                  data['bloodgroup'], data['email'], data['contact'], data['pancard'], data['aadharcard'])
            return {
                "success":  True
            }
        return {
            "NotFoundError": {
                "success":  False,
                "error": "Employee Not Found"
            }
        }


class EmployeeAddressDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('city', type=str, required=True,
                       help='city is required')
    parse.add_argument('state', type=str, required=True,
                       help='state is required')
    parse.add_argument('pincode', type=str, required=True,
                       help='pincode is required')
    parse.add_argument('fulladdress', type=str, required=True,
                       help='fulladdress is required')

    @jwt_required
    def get(self):
        empaddress = AddressModel.find_by_id(get_jwt_identity())
        if empaddress:
            return empaddress.json()
        return {"success": False, "error": "Not Found"}

    @jwt_required
    def post(self):
        data = EmployeeAddressDetails.parse.parse_args()
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            address = AddressModel(get_jwt_identity(
            ), data['city'], data['state'], data['pincode'], data['fulladdress'])
            address.save_to_db()
            return {
                "success": True
            }

        return{
            "success": False,
            "error": "Not Found"
        }

    @jwt_required
    def put(self):
        data = EmployeeAddressDetails.parse.parse_args()
        employee = AddressModel.find_by_id(get_jwt_identity())
        if employee:
            employee.update_to_db(
                data['city'], data['state'], data['pincode'], data['fulladdress'])
            return {
                "success": True
            }

        return{
            "success": False,
            "error": "Not Found"
        }


class EmployeeQualificationDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('qualification', type=str, required=True,
                       help='qualification is required')
    parse.add_argument('pass_year', type=int, required=True,
                       help='passyear is required')
    parse.add_argument('experience', type=float, required=True,
                       help='experience is required')

    @jwt_required
    def get(self):
        qualification = QualificationModel.find_by_id(get_jwt_identity())
        if qualification:
            return qualification.json()
        return {"success": False, "error": "Not Found"}

    @jwt_required
    def post(self):
        data = EmployeeQualificationDetails.parse.parse_args()
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            qualification = QualificationModel(get_jwt_identity(
            ), data['qualification'], data['pass_year'], data['experience'])
            qualification.save_to_db()
            return {"success":  True}

        return {"success": False, "error": "Not Found"}

    @jwt_required
    def put(self):
        data = EmployeeQualificationDetails.parse.parse_args()
        employee = QualificationModel.find_by_id(get_jwt_identity())
        if employee:
            employee.update_to_db(
                data['qualification'], data['pass_year'], data['experience'])
            return {"success":  True}

        return {"success": False, "error": "Not Found"}


class EmployeeSalaryDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('accountno', type=str, required=True,
                       help='accountno is required')
    parse.add_argument('ifsccode', type=str, required=True,
                       help='ifsccode is required')
    parse.add_argument('bankname', type=str, required=True,
                       help='bankname is required')
    parse.add_argument('pfaccount_no', type=str, required=True,
                       help='pfaccount_no is required')
    parse.add_argument('esi_no', type=str, required=True,
                       help='esi_no is required')

    @jwt_required
    def get(self):
        empsal = EmployeeSalaryDetailsModel.find_by_id(get_jwt_identity())
        if empsal:
            return empsal.json()
        return {"success": False, "error": "Not Found"}

    @jwt_required
    def post(self):
        data = EmployeeSalaryDetails.parse.parse_args()
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            salary = EmployeeSalaryDetailsModel(get_jwt_identity(
            ), data['accountno'], data['ifsccode'], data['bankname'], data['pfaccount_no'], data['esi_no'])
            salary.save_to_db()
            return {"success": True}
        return {"success": False, "error": "Not Found"}

    @jwt_required
    def put(self):
        data = EmployeeSalaryDetails.parse.parse_args()
        employee = EmployeeSalaryDetailsModel.find_by_id(get_jwt_identity())
        if employee:
            employee.update_to_db(data['accountno'], data['ifsccode'],
                                  data['bankname'], data['pfaccount_no'], data['esi_no'])
            return {"success": True}
        return {"success": False, "error": "Not Found"}


class EmployeeJoiningDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('accountno', type=str, required=True,
                       help='accountno is required')

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class EmployeeGradeDetails(Resource):
    pass


class Employee(Resource):
    @jwt_required
    def get(self):
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        return {
            "Employee":  employee.json(),
            "personalDetails": PersonalDetailsModel.find_by_id(get_jwt_identity()).json(),
            "AddressDetails": AddressModel.find_by_id(get_jwt_identity()).json(),
            "QualificationDetails": QualificationModel.find_by_id(get_jwt_identity()).json(),
            "SalaryInformation": EmployeeSalaryDetailsModel.find_by_id(get_jwt_identity()).json(),
            "success": True
        }
