# from app import app
# from config import db

# db.init_app(app)

# @app.before_first_request
# def init_db():
#     db.create_all()
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.secret_key = 'EmployeeManagementSystem'


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


app.run()
