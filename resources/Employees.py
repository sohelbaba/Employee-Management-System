from flask_restful import Resource, reqparse
from models.Employee import (
    AuthenticationModel,
    PersonalDetailsModel,
    AddressModel,
    QualificationModel,
    EmployeeSalaryDetailsModel,
    JoiningDetailsModel,
    Annual_Leave,
    GradeModel,
)
from models.Attendance import AttendanceModel
from models.Designation import DesignationModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    get_raw_jwt,
)
from blacklist import blacklist
from datetime import datetime, date
from customeDecorators import admin_required, Hr_required, Authentication_required
from sqlalchemy import and_
from app_init import mail
from flask_mail import Message


class EmployeeRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True,
                       help="username is required")
    parse.add_argument("password", type=str, required=True,
                       help="password is required")
    parse.add_argument("role", type=str, required=True,
                       help="role is required")
    parse.add_argument("joiningdate", type=str, required=True,
                       help="joining Date  is required")
    parse.add_argument("designation", type=str, required=True,
                       help="designation is required")
    parse.add_argument('email', type=str, required=True,
                       help='email is required')

    @Authentication_required
    def post(self):
        data = EmployeeRegister.parse.parse_args()
        employee = AuthenticationModel.find_by_username(data["username"])

        if employee:
            return {
                "AlreadyExistsError": {
                    "status": False,
                    "error": "Username already exists",
                }
            }

        joindate = date.fromisoformat(data['joiningdate'].split('T')[0])

        employee = AuthenticationModel(
            data['username'], data['password'], data['role'], data['email'], joindate)
        employee.save_to_db()

        # add  joining details

        joiningdetails = JoiningDetailsModel(employee.id, joindate)
        print(joiningdetails.json())
        joiningdetails.save_to_db()

        # fetch basic for particular designation
        des = DesignationModel.find_by_designation(data['designation'])
        print(des.json())

        # add employee level grade
        grade = GradeModel(
            employee.id, data['designation'], joindate, des.basic)
        grade.save_to_db()

        print(grade.json())

        # annual leave
        annual_leave = Annual_Leave(employee.id)
        annual_leave.save_to_db()

        # credential sent to user via email
        msg = Message('Welcome to LaNet Teams!', recipients=[data['email']])
        msg.body = '''
        Hello  ''' + data['username'].split('.')[0] + ''',
        We are delighted to have you among us as a part of La net team software solutions Pvt. Ltd.
        On behalf of all the members and the management, we would like to extend our warmest welcome and good wishes! Your Joining date will be ''' + data['joiningdate'].split('T')[0] + ''' .\n

        Here your credential for Company HRMS System.            
        username = ''' + data['username'] + '''
        password = ''' + data['password'] + '''
        HRMS Link = 'http://127.0.0.1:3000/'

        If you have any queries, please feel free to contact the Human Resources  Department. 
        We look forward to your success in the company\n

        Thanks & Regards,
        Name of hr
        HR Executive 
        Direct: +91 6353235503 | W: www.lanetteam.com 
        406, Luxuria Business Hub, Nr. VR Mall, Surat, Gujarat - 395007
        Ground Floor, I.T.P.I Building, Beside Celebration Mall, Bhuwana, Udaipur, Rajasthan - 313001'''
        mail.send(msg)

        return {
            "success": True,
            "message": "Employee Registerd",
            "id": employee.id,
            "Employee": employee.json()
        }


class JoiningDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True,
                       help="Username required")
    parse.add_argument(
        "joining_date", type=str, required=True, help="joining date required"
    )
    parse.add_argument("grade", type=str, required=True,
                       help="grade is required")
    parse.add_argument("basic", type=float, required=True,
                       help="basic is required")

    @Authentication_required
    def post(self):
        data = JoiningDetails.parse.parse_args()
        employee = AuthenticationModel.find_by_username(data["username"])
        if employee:
            joining_date = datetime.strptime(data["joining_date"], "%d %B %Y")
            joining_details = JoiningDetailsModel(
                employee.id,
                joining_date,
            )
            joining_details.save_to_db()

            # here grade details
            grade = GradeModel(
                employee.id, data["grade"], data["joining_date"], data["basic"]
            )
            grade.save_to_db()

            # here annual leave is set
            annual_leave = Annual_Leave(employee.id)
            annual_leave.save_to_db()

            return {"status": True}
        else:
            return {"error": data["username"] + "not Found"}


class EmployeeLogin(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("username", type=str, required=True,
                       help="username is required")
    parse.add_argument("password", type=str, required=True,
                       help="password is required")

    def post(self):
        data = EmployeeLogin.parse.parse_args()
        employee = AuthenticationModel.find_by_username(data["username"])
        # if employee.isAuthenticate:
        #     return {
        #         "success": False,
        #         "error": "You Are Already LoggedIn In Another System Please Logout there.."
        #     }

        if employee and safe_str_cmp(data["password"], employee.password):
            # chnage isauthenticate value
            employee.isAuthenticate = True
            Attend = AttendanceModel(
                employee.id,
                datetime.now().strftime("%H:%M:%S"),
                datetime.today().strftime("%d/%m/%Y"),
            )
            Attend.save_to_db()

            # print(employee.id)
            return {
                "access_token": create_access_token(
                    identity=employee.id, expires_delta=False
                ),
                "role": employee.role,
                "success": True,
                "authenticate": employee.isAuthenticate,
            }
        return {"error": "Username or password incorrent", "success": False}


class EmployeePersonalDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        "firstname", type=str, required=True, help="firstname is 11required"
    )
    parse.add_argument("lastname", type=str, required=True,
                       help="lastname is required")
    parse.add_argument("gender", type=str, required=True,
                       help="gender is required")
    parse.add_argument("dob", type=str, required=True, help="dob is required")
    parse.add_argument(
        "bloodgroup", type=str, required=True, help="bloodgroup is required"
    )
    parse.add_argument("email", type=str, required=True,
                       help="email is required")
    parse.add_argument("contactno", type=str, required=True,
                       help="contact is required")
    parse.add_argument(
        "pancardno", type=str, required=True, help="pancard no is required"
    )
    parse.add_argument(
        "aadharcardno", type=str, required=True, help="aadharcard no is required"
    )

    @jwt_required
    def get(self):
        employee_personal_details = PersonalDetailsModel.find_by_id(
            get_jwt_identity())
        if employee_personal_details:
            return employee_personal_details.json()
        return {"error": "Data not found", "success": False}

    @jwt_required
    def post(self):
        data = EmployeePersonalDetails.parse.parse_args()
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            personaldetails = PersonalDetailsModel(get_jwt_identity(), **data)
            personaldetails.save_to_db()
            return {"success": True}
        return {"NotFoundError": {"success": False, "error": "Employee Not Found"}}

    @jwt_required
    def put(self):
        data = EmployeePersonalDetails.parse.parse_args()
        employee = PersonalDetailsModel.find_by_id(get_jwt_identity())
        if employee:
            employee.update_to_db(
                data["firstname"],
                data["lastname"],
                data["gender"],
                data["dob"],
                data["bloodgroup"],
                data["email"],
                data["contactno"],
                data["pancardno"],
                data["aadharcardno"],
            )
            return {"success": True, "data": employee.json()}
        else:
            personaldetails = PersonalDetailsModel(
                get_jwt_identity(),
                data["firstname"],
                data["lastname"],
                data["gender"],
                data["dob"],
                data["bloodgroup"],
                data["email"],
                data["contactno"],
                data["pancardno"],
                data["aadharcardno"],
            )
            personaldetails.save_to_db()

            return {"success": True}


class EmployeeAddressDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("city", type=str, required=True,
                       help="city is required")
    parse.add_argument("state", type=str, required=True,
                       help="state is required")
    parse.add_argument("pincode", type=str, required=True,
                       help="pincode is required")
    parse.add_argument(
        "fulladdress", type=str, required=True, help="fulladdress is required"
    )

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
            address = AddressModel(
                get_jwt_identity(),
                data["city"],
                data["state"],
                data["pincode"],
                data["fulladdress"],
            )
            address.save_to_db()
            return {"success": True}

        return {"success": False, "error": "Not Found"}

    @jwt_required
    def put(self):
        data = EmployeeAddressDetails.parse.parse_args()
        employee = AddressModel.find_by_id(get_jwt_identity())
        if employee:
            employee.update_to_db(
                data["city"], data["state"], data["pincode"], data["fulladdress"]
            )
            return {"success": True, "data": employee.json(), "updated": True}
        else:
            address = AddressModel(
                get_jwt_identity(),
                data["city"],
                data["state"],
                data["pincode"],
                data["fulladdress"],
            )
            address.save_to_db()
            return {"success": True, "data": address.json(), "updated": False}


class EmployeeQualificationDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        "qualification", type=str, required=True, help="qualification is required"
    )
    parse.add_argument(
        "pass_year", type=int, required=True, help="passyear is required"
    )
    parse.add_argument(
        "experience", type=float, required=True, help="experience is required"
    )

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
            qualification = QualificationModel(
                get_jwt_identity(),
                data["qualification"],
                data["pass_year"],
                data["experience"],
            )
            qualification.save_to_db()
            return {"success": True}

        return {"success": False, "error": "Not Found"}

    @jwt_required
    def put(self):
        data = EmployeeQualificationDetails.parse.parse_args()
        employee = QualificationModel.find_by_id(get_jwt_identity())
        if employee:
            employee.update_to_db(
                data["qualification"], data["pass_year"], data["experience"]
            )
            return {"success": True, "updated": True}
        else:
            qualification = QualificationModel(
                get_jwt_identity(),
                data["qualification"],
                data["pass_year"],
                data["experience"],
            )
            qualification.save_to_db()
            return {"success": True, "updated": False}


class EmployeeSalaryDetails(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument(
        "accountno", type=str, required=True, help="accountno is required"
    )
    parse.add_argument("ifsccode", type=str, required=True,
                       help="ifsccode is required")
    parse.add_argument("bankname", type=str, required=True,
                       help="bankname is required")
    parse.add_argument(
        "pfaccount_no", type=str, required=True, help="pfaccount_no is required"
    )
    parse.add_argument("esi_no", type=str, required=True,
                       help="esi_no is required")

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
            salary = EmployeeSalaryDetailsModel(
                get_jwt_identity(),
                data["accountno"],
                data["ifsccode"],
                data["bankname"],
                data["pfaccount_no"],
                data["esi_no"],
            )
            salary.save_to_db()
            return {"success": True}
        return {"success": False, "error": "Not Found"}

    @jwt_required
    def put(self):
        data = EmployeeSalaryDetails.parse.parse_args()
        employee = EmployeeSalaryDetailsModel.find_by_id(get_jwt_identity())
        if employee:
            # employee.update_to_db(data['accountno'], data['ifsccode'],
            #                       data['bankname'], data['pfaccount_no'], data['esi_no'])
            employee.account_no = data["accountno"]
            employee.ifsc_code = data["ifsccode"]
            employee.pfaccount_no = data["bankname"]
            employee.bankname = data["pfaccount_no"]
            employee.esi_no = data["esi_no"]
            employee.save_to_db()
            return {"success": True, "Updated": True}
        else:
            salary = EmployeeSalaryDetailsModel(
                get_jwt_identity(),
                data["accountno"],
                data["ifsccode"],
                data["bankname"],
                data["pfaccount_no"],
                data["esi_no"],
            )
            salary.save_to_db()
            return {"success": True, "Updated": False}


class EmployeeLogout(Resource):
    @jwt_required
    def get(self):
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            employee.isAuthenticate = False
            employee.save_to_db()
            jti = get_raw_jwt()["jti"]
            blacklist.add(jti)

            attend = AttendanceModel.query.filter(
                and_(
                    AttendanceModel.date == datetime.today().strftime("%d/%m/%Y"),
                    AttendanceModel.emp_id == get_jwt_identity(),
                )
            ).first()

            attend.endtime = datetime.now().strftime("%H:%M:%S")
            attend.save_to_db()

            return {
                "msg": "Successfully logged out",
                "authenticate": employee.isAuthenticate,
            }, 200
        else:
            return {"error": "error in logout"}


class Employee(Resource):
    @jwt_required
    def get(self):
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        return {"Employee": employee.json(), "success": True}


class AllEmployees(Resource):
    @Authentication_required
    def get(self):
        employees = [auth.json() for auth in AuthenticationModel.query.filter(
            AuthenticationModel.role != 'Admin')]
        return {"Employees": employees, "status": 200}


class ChangePassword(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("password", type=str, required=True,
                       help="password is required")

    @jwt_required
    def put(self):
        data = ChangePassword.parse.parse_args()
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            employee.password = data["password"]
            employee.save_to_db()
            return {"status": True}
        return {"Status": False}


class EmployeeGradeHistory(Resource):
    @jwt_required
    def get(self):
        grades = [grade.json() for grade in GradeModel.query.filter(
            GradeModel.emp_id == get_jwt_identity())]
        return{"Grades": grades}
