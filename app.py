from resources.Employees import (
    EmployeeRegister, EmployeeLogin, EmployeePersonalDetails, Employee, EmployeeQualificationDetails,
    EmployeeAddressDetails, EmployeeSalaryDetails, EmployeeLogout, JoiningDetails, AllEmployees)
from resources.Admin import Admin
from resources.setup import Setup

from resources.Designation import AllGrades
from resources.Leave import Leave, LeaveApply, Leaves

from resources.Task import Task, TaskList

from blacklist import blacklist

# app = Flask(__name__)
# app.secret_key = 'EmployeeManagementSystem'
from app_init import app, jwt, api


# set database url
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.before_first_request
def init_db():
    db.create_all()


# Setup Api
api.add_resource(Setup, '/setup')

# admin api
api.add_resource(Admin, '/register', '/delete')

# employee login / logout
api.add_resource(EmployeeLogin, '/employee/login')  # done
api.add_resource(EmployeeLogout, '/employee/logout')  # done

# employee profile
api.add_resource(EmployeePersonalDetails, '/employee/profile')  # done
api.add_resource(EmployeeAddressDetails, '/employee/address')  # done
api.add_resource(EmployeeQualificationDetails,
                 '/employee/qualification')  # done
api.add_resource(EmployeeSalaryDetails, '/employee/salaryinfo')  # done
api.add_resource(Employee, '/employee/details')  # done
api.add_resource(Leaves, '/employee/leaves')  # done

# employee task
api.add_resource(Task, '/employee/task/<int:id>', '/employee/task')  # done
api.add_resource(TaskList, '/employee/tasks')  # done

# employee leave
api.add_resource(Leave, '/employee/leave')  # done

# Hr Api's
api.add_resource(EmployeeRegister, '/employee/register',
                 '/employee/<string:username>')  # done
api.add_resource(AllEmployees, '/employee/data')  # done

api.add_resource(JoiningDetails, '/employee/joiningdetails')  # done
api.add_resource(AllGrades, '/designations')  # done
api.add_resource(LeaveApply, '/leave/apply')  # done


if __name__ == '__main__':
    from config import db
    db.init_app(app)
    app.run(debug=True)
