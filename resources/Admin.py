from flask_restful import Resource, reqparse
from models.Employee import AuthenticationModel
from flask_jwt_extended import jwt_required
from customeDecorators import admin_required


class Admin(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True,
                       help='username is required')
    parse.add_argument('password', type=str, required=True,
                       help='password is required')
    parse.add_argument('role', type=str, required=True,
                       help='role is required')

    @admin_required
    def post(self):
        data = Admin.parse.parse_args()
        employee = AuthenticationModel(**data)
        employee.save_to_db()

        return {
            "success": True,
            "username": employee.username,
            "password": employee.password
        }

    @admin_required
    def delete(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str, required=True,
                           help='username is required')
        data = parse.parse_args()
        employee = AuthenticationModel.find_by_username(data['username'])

        if employee:
            employee.delete_from_db()
            return {
                "status": 200,
                "message": "Account Deleted"
            }
        return{
            "status": 404,
            "NotFoundError": "Given Username data not Found.."
        }
