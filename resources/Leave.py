from flask_restful import reqparse, Resource
from models.Leave import LeaveModel
from models.Employee import Annual_Leave
from flask_jwt_extended import jwt_required, get_jwt_identity
from customeDecorators import admin_required, Hr_required, Authentication_required

import datetime
from datetime import date
from sqlalchemy import DateTime
from app_init import mail
from flask_mail import Message
from models.Employee import AuthenticationModel
from resources.leavemessage import leaveApprovedmessage, leaveCanclemessage, leaveForwardmessage
from sqlalchemy import and_
from dateutil import parser


class Leave(Resource):
    @jwt_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("ltype", type=str, required=True,
                           help="Leave Type Required")
        parse.add_argument(
            "startdate", type=str, required=True, help="start_date Type Required"
        )
        parse.add_argument(
            "enddate", type=str, required=True, help="end_date Type Required"
        )
        parse.add_argument("desc", type=str, required=True,
                           help="desc Type Required")

        data = parse.parse_args()
        employee = AuthenticationModel.find_by_id(get_jwt_identity())
        if employee:
            if employee.role == 'Hr':
                leave = LeaveModel(
                    get_jwt_identity(),
                    data["ltype"],
                    data["startdate"],
                    data["enddate"],
                    data["desc"],
                    'Forward'
                )
                leave.save_to_db()
            else:
                leave = LeaveModel(
                    get_jwt_identity(),
                    data["ltype"],
                    data["startdate"],
                    data["enddate"],
                    data["desc"],
                    'Pending'
                )
                leave.save_to_db()

        return {
            "status": 200,
            "data": [leave.json() for leave in LeaveModel.query.all()],
        }

    @jwt_required
    def get(self):
        leave = [leave.json() for leave in LeaveModel.query.all()]
        return {"Leaves": leave}


class LeaveApply(Resource):
    @Authentication_required
    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument(
            "status", type=str, required=True, help="status Type Required"
        )
        data = parse.parse_args()
        leave = LeaveModel.find_by_id(id)
        if leave:
            leave.status = data["status"]
            leave.senction_date = datetime.datetime.now()
            leave.senction_by_id = get_jwt_identity()
            leave.save_to_db()

            # credential sent to user via email
            msg = Message('Leave Application ' +
                          data['status'] + '!', recipients=[AuthenticationModel.find_by_id(leave.emp_id).email])
            username = AuthenticationModel.find_by_id(
                leave.emp_id).username.split('.')[0]

            if data['status'] == 'Approved':
                msg.body = leaveApprovedmessage(
                    username, leave.start_date, leave.end_date)
                # deduct leave from annual leave
                anuualeave = Annual_Leave.find_by_id(leave.emp_id)
                delta = parser.parse(leave.end_date) - \
                    parser.parse(leave.start_date)
                if anuualeave:
                    if leave.leave_type == 'PL':
                        anuualeave.pl = Annual_Leave.find_by_id(
                            leave.emp_id).pl - delta.days
                    elif leave.leave_type == 'CL':
                        anuualeave.cl = Annual_Leave.find_by_id(
                            leave.emp_id).cl - delta.days
                    elif leave.leave_type == 'SL':
                        anuualeave.sl = Annual_Leave.find_by_id(
                            leave.emp_id).sl - delta.days
                    else:
                        # deduct salary also
                        anuualeave.lwp = Annual_Leave.find_by_id(
                            leave.emp_id).lwp - delta.days

                anuualeave.save_to_db()
                # print(anuualeave.json())

            elif data['status'] == 'Cancle':
                msg.body = leaveCanclemessage(
                    username, leave.start_date, leave.end_date)
            else:
                msg.body = leaveForwardmessage(
                    username, leave.start_date, leave.end_date)

            mail.send(msg)


class ApplyLeaves(Resource):
    @jwt_required
    def get(self):
        leave = [leave.json() for leave in LeaveModel.query.filter(
            LeaveModel.emp_id == get_jwt_identity())]
        return {"Leaves": leave}


class Leaves(Resource):
    @jwt_required
    def get(self):
        leave = Annual_Leave.find_by_id(get_jwt_identity())
        return {"Leaves": leave.json()}


class AllLeaves(Resource):
    @Authentication_required
    def get(self):
        leave = [leave.json() for leave in LeaveModel.query.all()]
        return {"Leaves": leave}
