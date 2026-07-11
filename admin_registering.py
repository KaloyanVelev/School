import os
from flask.cli import load_dotenv
from werkzeug.security import generate_password_hash
from database import db
from models.user import UserModel
from models.enums import UserRole




def init_admin():

    load_dotenv()

    admin_first_name = os.getenv('ADMIN_FIRST_NAME')
    admin_last_name = os.getenv('ADMIN_LAST_NAME')
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')

    admin_exists = UserModel.query.filter_by(permission=UserRole.ADMIN).first()

    if admin_exists:
        print("[System Setup] Admin user already exists!")
        return

    if not admin_first_name or not admin_last_name or not admin_email or not admin_password:
        print('Please provide all required environment variables for the admin!')
        return



    print("[System Setup] No admin account detected!")
    print("[System Setup]Creating admin user using data from .env file...")

    hashed_password = generate_password_hash(admin_password)

    try:
        new_admin = UserModel(
            first_name = admin_first_name,
            last_name = admin_last_name,
            email = admin_email,
            password = hashed_password,
            permission = 'ADMIN'
        )
        db.session.add(new_admin)
        db.session.commit()

        print("[System Setup] Admin user created successfully!")
        print("[System Setup] Admin user details:")
        print(f"[System Setup] EMAIL: {admin_email}]")
        print(f"[System Setup] PASSWORD: {admin_password}]")

    except Exception as e:
        db.session.rollback()
        print("[ERROR] Failed to create initial admin user!")
