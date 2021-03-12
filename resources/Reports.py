from flask_restful import Resource, reqparse
from models.Employee import (
    AuthenticationModel,
    JoiningDetailsModel
)
from models.Task import TaskModel
from models.salary import SalaryModel
from models.Leave import LeaveModel
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_raw_jwt,
)
from datetime import date
import datetime
from customeDecorators import admin_required, Hr_required, Authentication_required
from sqlalchemy import and_


class EmployeeReport(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("fromdate", type=str, required=False,
                       help="from date is required")
    parse.add_argument("todate", type=str, required=False,
                       help="to date is required")

    @Authentication_required
    def post(self):
        data = EmployeeReport.parse.parse_args()

        fromDate = date.fromisoformat(data['fromdate'].split('T')[0])
        toDate = date.fromisoformat(data['todate'].split('T')[0])

        fromdate = fromDate.timetuple()
        fdate = datetime.datetime(fromdate[0], fromdate[1],
                                  fromdate[2], fromdate[3], fromdate[4])

        todate = toDate.timetuple()
        tdate = datetime.datetime(todate[0], todate[1],
                                  todate[2], todate[3], todate[4])

        employeereport = [employee.json() for employee in AuthenticationModel.query.filter(
            AuthenticationModel.role != 'Admin', AuthenticationModel.join_date.between(fdate, tdate))]

        return{'status': 'Succes', 'Employee': employeereport}


class TaskReport(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("fromdate", type=str, required=False,
                       help="from date is required")
    parse.add_argument("todate", type=str, required=False,
                       help="to date is required")

    def post(self):
        data = EmployeeReport.parse.parse_args()

        fromDate = date.fromisoformat(data['fromdate'].split('T')[0])
        toDate = date.fromisoformat(data['todate'].split('T')[0])

        fromdate = fromDate.timetuple()
        fdate = datetime.datetime(fromdate[0], fromdate[1],
                                  fromdate[2], fromdate[3], fromdate[4])

        todate = toDate.timetuple()
        tdate = datetime.datetime(todate[0], todate[1],
                                  todate[2], todate[3], todate[4])

        tasks = [task.json() for task in TaskModel.query.filter(
            TaskModel.date.between(fdate, tdate))]
        return {"Tasks": tasks}


class SalaryReport(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("fromdate", type=str, required=False,
                       help="from date is required")
    parse.add_argument("todate", type=str, required=False,
                       help="to date is required")

    def post(self):
        data = EmployeeReport.parse.parse_args()

        fromDate = date.fromisoformat(data['fromdate'].split('T')[0])
        toDate = date.fromisoformat(data['todate'].split('T')[0])

        fromdate = fromDate.timetuple()
        fdate = datetime.datetime(fromdate[0], fromdate[1],
                                  fromdate[2], fromdate[3], fromdate[4])

        todate = toDate.timetuple()
        tdate = datetime.datetime(todate[0], todate[1],
                                  todate[2], todate[3], todate[4])

        salaryreport = [salary.json() for salary in SalaryModel.query.filter(
            SalaryModel.generateddate.between(fdate, tdate))]
        return {'Salary': salaryreport}


class LeaveReport(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument("fromdate", type=str, required=False,
                       help="from date is required")
    parse.add_argument("todate", type=str, required=False,
                       help="to date is required")

    def post(self):
        data = SalaryReport.parse.parse_args()

        fromDate = date.fromisoformat(data['fromdate'].split('T')[0])
        toDate = date.fromisoformat(data['todate'].split('T')[0])

        fromdate = fromDate.timetuple()
        fdate = datetime.datetime(fromdate[0], fromdate[1],
                                  fromdate[2], fromdate[3], fromdate[4])

        todate = toDate.timetuple()
        tdate = datetime.datetime(todate[0], todate[1],
                                  todate[2], todate[3], todate[4])

        leavereport = [leave.json() for leave in LeaveModel.query.filter(
            LeaveModel.apply_date.between(fdate, tdate))]
        return {'Leave': leavereport}
