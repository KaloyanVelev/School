from flask import Flask
from database import db
from resources.routes import app_bp
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:5432/postgres'
    app.config['SECRET_KEY'] = "52f0c854e544f440769cba3b9c4405bd8d791f0dd5c6d5a3673eba39146bec40"


    db.init_app(app)
    app.register_blueprint(app_bp)

    return app


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)