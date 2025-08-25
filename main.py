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

from libs.database import init_db

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.app_manager import app_manager
from views.auth_window import Auth
from views.register_window import Register


# from controllers.crud import load_user_session, check_if_logged_in

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.init_database()
        # Создаем только окна авторизации/регистрации
        self.auth_window = Auth()
        self.register_window = Register()

        # Подключаем сигналы менеджера
        self.connect_signals()

        # Проверяем авторизацию
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
        # Подключаем только базовые сигналы переключения
        app_manager.show_auth_signal.connect(self.show_auth)
        app_manager.show_reg_signal.connect(self.show_reg)

    def check_authentication(self):
        # Раскомментируйте когда будет готова БД
        # session_data = load_user_session()
        # if session_data and session_data.get("user_id"):
        #     user_id = check_if_logged_in()
        #     if user_id:
        #         # Автоматический вход через auth_window
        #         self.auth_window.show_main_window(user_id)
        #         return

        # Показываем окно авторизации по умолчанию
        self.auth_window.show_window()

    def show_auth(self):
        self.register_window.hide()
        self.auth_window.show_window()

    def show_reg(self):
        self.auth_window.hide()
        self.register_window.show_window()

    def run(self):
        return self.app.exec()


if __name__ == "__main__":
    main_app = MainApp()
    sys.exit(main_app.run())