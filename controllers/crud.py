import json
import os
from sqlalchemy import func, and_, case
from sqlalchemy.orm import Session
from libs.database import SessionLocal
from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash


def save_user_session(user_id):
    with open("libs/user_session.json", "w") as f:
        json.dump({"user_id": user_id}, f)


def delete_user_session():
    auth_file_path = "libs/user_session.json"
    if os.path.exists(auth_file_path):
        os.remove(auth_file_path)


def load_user_session():
    try:
        with open("libs/user_session.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def check_if_logged_in():
    session_data = load_user_session()
    if session_data:
        user_id = session_data.get("user_id")
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        if user:
            return user.id, user.is_admin
    return None, None


def authenticate_user(login, password):
    session = SessionLocal()
    user = session.query(User).filter_by(login=login).first()
    session.close()
    if user and check_password_hash(user.password, password):
        return user
    return None


def create_user(last_name, first_name, middle_name, phone, login,
                password, is_admin):
    session = SessionLocal()

    hashed_password = generate_password_hash(password)
    new_user = User(
        last_name=last_name,
        first_name=first_name,
        middle_name=middle_name,
        phone=phone,
        login=login,
        password=hashed_password,
        is_admin=is_admin
    )
    session.add(new_user)
    session.commit()
    session.close()
    return new_user