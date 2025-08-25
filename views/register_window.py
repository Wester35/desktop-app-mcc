from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit
from PySide6.QtCore import Qt

from controllers.crud import create_user
# from controllers.crud import create_user_with_group
from ui.ui_register import Ui_Registration as RegisterUI
from views.app_manager import app_manager


class Register(QWidget):
    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlag(Qt.Window)

        self.ui = RegisterUI()
        self.ui.setupUi(self)
        self.connect_signals()


        self.setWindowIcon(QPixmap("ui/resources/app_icon.png"))
        self.background = QLabel(self.ui.frame_2)
        self.background.setGeometry(0, 0, 650, 720)

        pixmap = QPixmap("ui/resources/background.jpg")
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.lower()
        self.ui.checkPassword.setText("👁️‍🗨️")
        self.ui.checkPassword.setCheckable(True)


    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.handle_register)
        self.ui.checkPassword.clicked.connect(self.check_pwd)
        self.ui.to_auth.clicked.connect(self.go_to_auth)

        app_manager.show_reg_signal.connect(self.show_window)

    def go_to_auth(self):
        self.hide()
        app_manager.show_auth_signal.emit()

    def parse_fullname(self, full_name):
            parts = full_name.strip().split()
            return (
                parts[0] if len(parts) > 0 else "",
                parts[1] if len(parts) > 1 else "",
                parts[2] if len(parts) > 2 else "",
            )

    def handle_register(self):
        login = self.ui.usernameEdit.text()
        last, first, middle = self.parse_fullname(self.ui.fioEdit.text())
        phone = self.ui.phoneEdit.text()
        password = self.ui.passwordEdit.text()
        password_2 = self.ui.passwordEdit_2.text()

        if password != password_2:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают!")
            return

        if not login or not last or not first or not phone or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        try:
            create_user(
                last_name=last,
                first_name=first,
                middle_name=middle,
                phone=phone,
                login=login,
                password=password
            )
            QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован")
            self.go_to_auth()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка БД: {str(e)}")


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
        self.ui.usernameEdit.clear()
        self.ui.passwordEdit.clear()
        self.ui.checkPassword.setChecked(False)
        self.ui.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)