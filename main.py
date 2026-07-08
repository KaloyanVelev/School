from time import sleep

from flask import Flask
from database import db
from resources.routes import app_bp
from dotenv import load_dotenv
import os
import secrets
from admin_registering import init_admin
from models.enums import UserRole
from models.user import UserModel
from models.school import SchoolModel
from models.school_class import SchoolClassModel
from models.school_subject import SchoolSubjectModel
from models.student import StudentModel
from models.schedule import ScheduleModel
from models.remark import RemarkModel
from models.parent_student import ParentStudentModel
from models.grade import GradeModel

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

secret_key = os.getenv('SECRET_KEY')

if not secret_key:
    secret_key = secrets.token_hex(32)
    with open('.env', 'a') as f:
        f.write(f'\nSECRET_KEY={secret_key}\n')

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres'
    app.config['SECRET_KEY'] = f"{secret_key}"


    db.init_app(app)
    app.register_blueprint(app_bp)

    return app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_admin()
    app.run(debug=True)