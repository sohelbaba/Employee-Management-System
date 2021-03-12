from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.Task import TaskModel
from customeDecorators import Authentication_required
import datetime as DT


class Task(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument(
        "technology", type=str, required=True, help="technology is required"
    )
    parse.add_argument(
        "projectname", type=str, required=True, help="projectname is required"
    )
    parse.add_argument("hour", type=int, required=True,
                       help="hour is required")
    parse.add_argument(
        "desc", type=str, required=True, help="task desc entry is required"
    )

    @jwt_required
    def get(self, id):
        task = TaskModel.find_by_id(id)
        if task:
            return {"task": task.json(), "status": 200}
        return {"Error": "Not Found", "status": 400}

    @jwt_required
    def post(self):
        data = Task.parse.parse_args()
        task = TaskModel(
            get_jwt_identity(),
            data["technology"],
            data["projectname"],
            data["hour"],
            data["desc"],
        )
        task.save_to_db()
        return {"status": 201, "new": False, "Employee": get_jwt_identity()}

    @jwt_required
    def put(self, id):
        TaskFind = TaskModel.find_by_id(id)
        if TaskFind:
            data = Task.parse.parse_args()
            TaskFind.technology = data["technology"]
            TaskFind.projectname = data["projectname"]
            TaskFind.hour = data["hour"]
            TaskFind.desc = data["desc"]
            TaskFind.save_to_db()
            return {"status": 200, "updated": True, "data": TaskFind.json()}

    def delete(self, id):
        task = TaskModel.find_by_id(id)
        if task:
            task.delete_from_db()
            return {"status": True, "Message": "Deleted"}


class TaskList(Resource):
    @jwt_required
    def get(self):
        tasks = [
            task.json() for task in TaskModel.query.filter_by(emp_id=get_jwt_identity())
        ]
        return {"Tasks": tasks}


class AllTaskList(Resource):
    @Authentication_required
    def get(self):
        today = DT.date.today()
        week_ago = today - DT.timedelta(days=7)

        tasks = [task.json() for task in TaskModel.query.all()]
        return {"Tasks": tasks}
