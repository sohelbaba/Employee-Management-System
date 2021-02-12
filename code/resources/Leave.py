from flask_restful import reqparse, Resource
from models.Leave import LeaveModel
from models.Employee import Annual_Leave
from flask_jwt_extended import jwt_required, get_jwt_identity
from customeDecorators import admin_required, Hr_required

import datetime
from sqlalchemy import DateTime


class Leave(Resource):

    @jwt_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('leave_type', type=str, required=True,
                           help='Leave Type Required')
        parse.add_argument('start_date', type=str,
                           required=True, help='start_date Type Required')
        parse.add_argument('end_date', type=str,
                           required=True, help='end_date Type Required')
        parse.add_argument('desc', type=str,
                           required=True, help='desc Type Required')
        data = parse.parse_args()
        leave = LeaveModel(get_jwt_identity(), data['leave_type'],
                           data['start_date'], data['end_date'])
        leave.save_to_db()
        return {'status': 200}

    @jwt_required
    def get(self):
        leave = [leave.json() for leave in LeaveModel.query.all()]
        return {'Leaves': leave}


class LeaveApply(Resource):
    @Hr_required
    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('status', type=str,
                           required=True, help='status Type Required')
        data = parse.parse_args()
        leave = LeaveModel.find_by_id(id)
        if leave:
            leave.status = data['status']
            leave.senction_date = datetime.datetime.utcnow
            leave.senction_by_id = get_jwt_identity()
            leave.save_to_db()


class Leaves(Resource):
    @jwt_required
    def get(self):
        leave = Annual_Leave.find_by_id(get_jwt_identity())
        if leave:
            return {'Leaves': leave.json()}
        return {"Status": 404}
