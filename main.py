from flask import Flask
from database import db
from resources.routes import app_bp
from dotenv import load_dotenv
import os
import secrets

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
    app.run(debug=True)