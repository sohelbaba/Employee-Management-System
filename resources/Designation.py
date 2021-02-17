from flask_restful import Resource, reqparse
from models.Designation import DesignationModel
from flask_jwt_extended import jwt_required


class AllGrades(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('designation', type=str,
                       required=True, help='designation required')
    parse.add_argument('basic', type=float, required=True,
                       help='basic required')

    @jwt_required
    def post(self):
        try:
            data = AllGrades.parse.parse_args()
            # data['designation'] , data['basic']
            grade = DesignationModel(**data)
            grade.save_to_db()
            return {'status': 201}
        except:
            return {'status': 401}
