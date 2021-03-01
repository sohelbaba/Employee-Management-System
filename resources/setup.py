from flask_restful import Resource, reqparse
from models.Employee import AuthenticationModel


class Setup(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username', type=str, required=True,
                       help='username is required')
    parse.add_argument('password', type=str, required=True,
                       help='password is required')
    parse.add_argument('role', type=str, required=True,
                       help='role is required')
    parse.add_argument('email', type=str, required=True,
                       help='email is required')

    def post(self):
        data = Setup.parse.parse_args()
        employee = AuthenticationModel(**data)
        employee.save_to_db()

        return {
            "success": True,
            "username": employee.username,
            "password": employee.password
        }
