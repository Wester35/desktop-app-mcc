import sys
import os
from PySide6.QtWidgets import QApplication

from controllers.crud import check_if_logged_in, load_user_session, create_user, check_existing_admin
from libs.database import init_db
from views.main_window import MainWindow

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from os import getenv
from dotenv import load_dotenv
from PySide6.QtWidgets import QMessageBox
from views.app_manager import app_manager
from views.auth_window import Auth


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        load_dotenv()
        self.init_database()
        self.init_admin()
        self.auth_window = Auth()
        self.main_window = None
        self.session_was_saved = False
        self.connect_signals()
        self.check_authentication()

    def init_database(self):
        try:
            init_db()
            print("База данных успешно инициализирована")
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")
            QMessageBox.critical(None, "Ошибка БД", f"Не удалось инициализировать базу данных: {e}")

    def init_admin(self):
        try:
            check = check_existing_admin()
            if check:
                create_user(
                    last_name="",
                    first_name="",
                    middle_name="",
                    phone="",
                    login=getenv('login'),
                    password=getenv('password'),
                    is_admin=True
                )
                print("Администратор успешно инициализирован")
        except Exception as e:
            print(f"Ошибка инициализации администратора: {e}")
            QMessageBox.critical(None, "Ошибка БД", f"Не удалось инициализировать администратора: {e}")

    def connect_signals(self):
        app_manager.show_main_signal.connect(self.show_main_window)
        app_manager.logout_signal.connect(self.handle_logout)

    def check_authentication(self):
        session_data = load_user_session()
        print(f"Session data: {session_data}")

        if session_data and session_data.get("user_id"):
            user_id, is_admin = check_if_logged_in()
            print(f"Auto-login user: {user_id}, admin: {is_admin}")

            if user_id:
                self.session_was_saved = True
                self.auth_window.hide()
                print("Auth window hidden")
                self.show_main_window(user_id, is_admin)
                return

        print("No saved session, showing auth window")
        self.auth_window.show_window()

    def show_main_window(self, user_id, is_admin):
        self.auth_window.hide()

        if self.main_window is None:
            self.main_window = MainWindow(user_id, is_admin)
            app_manager.logout_signal.disconnect(self.handle_logout)
        else:
            self.main_window.update_user_data(user_id, is_admin)

        self.main_window.show()

    def handle_logout(self, session_was_saved):
        if self.main_window:
            self.main_window.hide()
            self.main_window = None

        self.session_was_saved = session_was_saved

        if not session_was_saved:
            self.auth_window.handle_logout(session_was_saved)
            self.auth_window.show_window()
        else:
            QApplication.quit()

    def run(self):
        return self.app.exec()


if __name__ == "__main__":
    main_app = MainApp()
    sys.exit(main_app.run())