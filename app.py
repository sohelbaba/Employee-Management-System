from flask_migrate import Migrate
from config import db
from resources.Employees import (
    EmployeeRegister,
    EmployeeLogin,
    EmployeePersonalDetails,
    Employee,
    EmployeeQualificationDetails,
    EmployeeAddressDetails,
    EmployeeSalaryDetails,
    EmployeeLogout,
    JoiningDetails,
    AllEmployees,
    ChangePassword,
    EmployeeGradeHistory
)
from resources.Admin import Admin
from resources.setup import Setup
from resources.salary import Salary, SalaryDetails, EmployeeSalaryList

from resources.Designation import AllGrades
from resources.Leave import Leave, LeaveApply, Leaves, AllLeaves, ApplyLeaves

from resources.Task import Task, TaskList, AllTaskList
from blacklist import blacklist

from resources.Reports import EmployeeReport, TaskReport, SalaryReport, LeaveReport

# app = Flask(__name__)
# app.secret_key = 'EmployeeManagementSystem'
from app_init import app, jwt, api, mail


# set database url
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in blacklist


@app.before_first_request
def init_db():
    db.create_all()


# Setup Api
api.add_resource(Setup, "/setup")

# admin api
api.add_resource(Admin, "/register", "/delete")

# employee login / logout
api.add_resource(EmployeeLogin, "/employee/login")  # done
api.add_resource(EmployeeLogout, "/employee/logout")  # done
api.add_resource(ChangePassword, "/employee/changepassword")

# employee profile
api.add_resource(EmployeePersonalDetails, "/employee/profile")  # done
api.add_resource(EmployeeAddressDetails, "/employee/address")  # done
api.add_resource(EmployeeQualificationDetails,
                 "/employee/qualification")  # done
api.add_resource(EmployeeSalaryDetails, "/employee/salaryinfo")  # done
api.add_resource(Employee, "/employee/details")  # done
api.add_resource(Leaves, "/employee/leaves")  # done

# employee task
api.add_resource(Task, "/employee/task/<int:id>", "/employee/task")  # done
api.add_resource(TaskList, "/employee/tasks")  # done
api.add_resource(AllTaskList, "/employee/Alltasks")

# employee leave
api.add_resource(Leave, "/employee/leave")  # done
api.add_resource(AllLeaves, '/employee/AllLeaves')
api.add_resource(ApplyLeaves, '/employee/applyleaves')

api.add_resource(EmployeeSalaryList, '/employee/salarydetails')
api.add_resource(EmployeeGradeHistory, '/employee/gradeshistory')

# Hr Api's
api.add_resource(
    EmployeeRegister, "/employee/register", "/employee/<string:username>"
)  # done
api.add_resource(AllEmployees, "/employee/data")  # done

api.add_resource(JoiningDetails, "/employee/joiningdetails")  # done
api.add_resource(AllGrades, "/designations", "/getdesignation")  # done
api.add_resource(LeaveApply, "/leave/<int:id>")  # done
api.add_resource(Salary, '/employee/salarygenerate')
api.add_resource(SalaryDetails, '/salarydetails')


# report's
api.add_resource(EmployeeReport, '/employee/reports')
api.add_resource(TaskReport, '/task/reports')
api.add_resource(SalaryReport, '/salary/reports')
api.add_resource(LeaveReport, '/leave/reports')

migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db, render_as_batch=True)

if __name__ == "__main__":
    app.run(debug=True)
