from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'EmployeeManagementSystem'


api = Api(app)
jwt = JWTManager(app)
