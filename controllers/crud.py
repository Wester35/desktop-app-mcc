import json
import os
from sqlalchemy import func, and_, case
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from cryptography.fernet import Fernet
from pathlib import Path
from libs.database import SessionLocal
from models.User import User



def generate_key():
    return Fernet.generate_key()


def update_forecasts(new_integral=None, new_interval=None, filename=Path(__file__).parent.parent.absolute()
                                                                    / 'data/forecasts.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = {}

    if new_integral is not None:
        data["integral"] = new_integral

    if new_interval is not None:
        data["interval"] = new_interval

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return data

def get_session_path():
    app_data_dir = Path.home() / ".mcc_app"
    app_data_dir.mkdir(exist_ok=True)
    return app_data_dir / "session.dat"


def get_encryption_key():
    key_file = get_session_path().parent / "key.dat"

    if key_file.exists():
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key


def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data


def save_user_session(user_id, remember_me=False):
    try:
        session_data = {
            'user_id': user_id,
            'login_time': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=30)).isoformat() if remember_me else None,
            'remember_me': remember_me
        }

        key = get_encryption_key()
        encrypted_data = encrypt_data(json.dumps(session_data), key)

        session_path = get_session_path()
        with open(session_path, 'wb') as f:
            f.write(encrypted_data)

        os.chmod(session_path, 0o600)

        return True
    except Exception as e:
        print(f"Ошибка сохранения сессии: {e}")
        return False


def load_user_session():
    try:
        session_path = get_session_path()
        if not session_path.exists():
            return None

        key = get_encryption_key()

        with open(session_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = decrypt_data(encrypted_data, key)
        session_data = json.loads(decrypted_data)

        if session_data['remember_me'] and session_data['expires_at']:
            expires_at = datetime.fromisoformat(session_data['expires_at'])
            if datetime.now() > expires_at:
                delete_user_session()
                return None

        return session_data

    except Exception as e:
        print(f"Ошибка загрузки сессии: {e}")
        # При ошибках удаляем поврежденную сессию
        delete_user_session()
        return None


def delete_user_session():
    try:
        session_path = get_session_path()
        if session_path.exists():
            session_path.unlink()
        return True
    except Exception as e:
        print(f"Ошибка удаления сессии: {e}")
        return False


def check_if_logged_in():
    session_data = load_user_session()
    if not session_data:
        return None, False

    from libs.database import SessionLocal

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == session_data['user_id']).first()
        if user:
            return user.id, user.is_admin
        else:
            delete_user_session()
            return None, False
    finally:
        db.close()


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

def check_existing_admin():
    db = SessionLocal()
    existing_admin = db.query(User).filter(User.is_admin == True).first()
    db.close()

    if existing_admin:
        print("Администратор уже существует, пропускаем инициализацию")
        return False

    return True


def get_user_data(user_id):
    """Получение данных пользователя по ID"""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user_data = {
                'id': user.id,
                'login': user.login,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'phone': user.phone,
                'is_admin': user.is_admin,
            }
            return user_data
        else:
            return None
    except Exception as e:
        print(f"Ошибка получения данных пользователя: {e}")
        return None
    finally:
        session.close()


def update_user_password(user_id, current_password, new_password):
    """Обновление пароля пользователя"""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Проверяем текущий пароль
        if not check_password_hash(user.password, current_password):
            return False

        # Хешируем новый пароль
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password

        session.commit()
        return True

    except Exception as e:
        print(f"Ошибка изменения пароля: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def get_user_full_name(user_id):
    """Получение полного имени пользователя"""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            # Собираем полное имя из компонентов
            name_parts = []
            if user.last_name:
                name_parts.append(user.last_name)
            if user.first_name:
                name_parts.append(user.first_name)
            if user.middle_name:
                name_parts.append(user.middle_name)

            return ' '.join(name_parts) if name_parts else user.login
        else:
            return "Неизвестный пользователь"
    except Exception as e:
        print(f"Ошибка получения имени пользователя: {e}")
        return "Ошибка загрузки"
    finally:
        session.close()