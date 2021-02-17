from app import app
from config import db

db.init_app(app)


@app.before_first_request
def init_db():
    db.create_all()
