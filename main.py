# import sys
# from PySide6.QtWidgets import QApplication
# from controllers.crud import load_user_session, check_if_logged_in
# from views.auth_window import Auth
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     session_data = load_user_session()
#     if session_data and session_data.get("user_id"):
#         user_id = check_if_logged_in()
#         # main_app = MainApp(user_id)
#         # main_app.show()
#     else:
#         main_app = Auth()
#         main_app.show()
#         pass
#     sys.exit(app.exec())

import sys
import os
from PySide6.QtWidgets import QApplication

from controllers.crud import check_if_logged_in, load_user_session
from libs.database import init_db
from views.main_window import MainWindow

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.app_manager import app_manager
from views.auth_window import Auth
from views.register_window import Register


# from controllers.crud import load_user_session, check_if_logged_in

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.init_database()
        self.auth_window = Auth()
        self.main_window = None
        self.connect_signals()
        self.check_authentication()

    def init_database(self):
        """Инициализация базы данных"""
        try:
            init_db()  # Создает таблицы если они не существуют
            print("База данных успешно инициализирована")
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")
            # Можно показать сообщение об ошибке
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Ошибка БД", f"Не удалось инициализировать базу данных: {e}")

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
                self.auth_window.hide()
                print("Auth window hidden")
                # Автоматически показываем главное окно
                self.show_main_window(user_id, is_admin)
                return

        print("No saved session, showing auth window")
        self.auth_window.show_window()

    def show_main_window(self, user_id, is_admin):
        self.auth_window.hide()

        # Создаем главное окно
        if self.main_window is None:
            self.main_window = MainWindow(user_id, is_admin)
            app_manager.logout_signal.disconnect(self.handle_logout)
        else:
            self.main_window.update_user_data(user_id, is_admin)

        # Показываем главное окно
        self.main_window.show()

    def handle_logout(self):
        if self.main_window:
            self.main_window.hide()
            self.main_window = None

        self.auth_window.handle_logout()
        self.auth_window.show_window()

    def run(self):
        return self.app.exec()


if __name__ == "__main__":
    main_app = MainApp()
    sys.exit(main_app.run())