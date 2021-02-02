from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.Task import TaskModel


class Task(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('task', type=str, required=True,
                       help='task entry is required')
    parse.add_argument('task_log', type=str, required=False,
                       help='task log is required')

    @jwt_required
    def get(self, id):
        task = TaskModel.find_by_id(id)
        if task:
            return {'task': task.json(), 'status': 200}
        return {'Error': 'Not Found', 'status': 400}

    @jwt_required
    def post(self):
        data = Task.parse.parse_args()
        task = TaskModel(get_jwt_identity(), data['task'], data['task_log'])
        task.save_to_db()
        return {'status': 201}

    @jwt_required
    def put(self, id):
        TaskFind = TaskModel.find_by_id(id)
        if TaskFind:
            data = Task.parse.parse_args()
            TaskFind.task = data['task']
            TaskFind.save_to_db()
            return {'status': 200}


class TaskList(Resource):
    @jwt_required
    def get(self):
        tasks = [task.json()
                 for task in TaskModel.query.filter_by(emp_id=get_jwt_identity())]
        return {'Tasks':  tasks}
