from flask_restful import Resource, reqparse
from models.Designation import DesignationModel
from flask_jwt_extended import jwt_required
from customeDecorators import admin_required, Authentication_required


class AllGrades(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('designation', type=str,
                       required=True, help='designation required')
    parse.add_argument('basic', type=float, required=True,
                       help='basic required')

    @admin_required
    def post(self):
        try:
            data = AllGrades.parse.parse_args()
            # data['designation'] , data['basic']
            grade = DesignationModel(data['designation'], data['basic'])
            grade.save_to_db()
            return {'status': 201}
        except:
            return {'status': 401}

    @Authentication_required
    def put(self):
        data = AllGrades.parse.parse_args()

        des = DesignationModel.find_by_designation(data['designation'])
        if des:
            des.basic = data['basic']
            des.save_to_db()
            return {'Status': 'updated'}

        return{'Status': 'NotFound'}

    @Authentication_required
    def get(self):
        designation = [desg.json() for desg in DesignationModel.query.all()]
        return {"designation": designation}
