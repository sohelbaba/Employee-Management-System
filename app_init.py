from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail

app = Flask(__name__)
CORS(app)
app.secret_key = 'EmployeeManagementSystem'


# set email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sohelmulla508@gmail.com'
app.config['MAIL_PASSWORD'] = 'S9714449348s'
app.config['MAIL_DEFAULT_SENDER'] = 'sohelmulla508@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


api = Api(app)
jwt = JWTManager(app)

mail = Mail(app)
