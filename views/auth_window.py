from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit
# from controllers.crud import authenticate_user, save_user_session
from ui.ui_auth import Ui_Authorization as LoginUI
from views.app_manager import app_manager
from views.main_window import MainWindow


class Auth(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = LoginUI()
        self.ui.setupUi(self)
        self.connect_signals()

        self.setWindowIcon(QPixmap("ui/resources/app_icon.png"))
        self.background = QLabel(self.ui.frame_2)
        self.background.setGeometry(0, 0, 600, 600)

        pixmap = QPixmap("ui/resources/background.jpg")
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.lower()
        self.ui.checkPassword.setText("👁️‍🗨️")
        self.ui.checkPassword.setCheckable(True)
        self.main_window = MainWindow()

    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.handle_login)
        self.ui.to_register.clicked.connect(self.go_to_register)
        self.ui.checkPassword.clicked.connect(self.check_pwd)
        app_manager.show_auth_signal.connect(self.show_window)
        app_manager.logout_signal.connect(self.handle_logout)

    def go_to_register(self):
        self.hide()
        app_manager.show_reg_signal.emit()

    def handle_login(self):
        login = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        # огда будет готова БД
        # user = authenticate_user(login, password)
        #
        # if user:
        #     if self.ui.checkBox.isChecked():
        #         save_user_session(user.id)
        #     self.show_main_window(user.id, user.is_teacher, user.is_admin)
        # else:
        #     QMessageBox.warning(self, "Ошибка", "Неверно")

        # Временная заглушка для теста
        self.show_main_window(1)

    def show_main_window(self, user_id):
        """Показать главное окно (вызывается только после успешной авторизации)"""
        self.hide()  # Скрываем окно авторизации

        # Создаем или показываем главное окно
        if self.main_window is None:
            self.main_window = MainWindow(user_id)
        else:
            # Обновляем данные если окно уже существует
            self.main_window.update_user_data(user_id)

        self.main_window.show()

    def check_pwd(self):
        if self.ui.checkPassword.isChecked():
            self.ui.passwordEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def handle_logout(self):
        """Обработка выхода - очистка полей"""
        self.ui.usernameEdit.clear()
        self.ui.passwordEdit.clear()
        self.ui.checkPassword.setChecked(False)
        self.ui.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)