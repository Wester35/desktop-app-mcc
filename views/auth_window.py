from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit

from controllers.crud import save_user_session, authenticate_user
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

        self.session_was_saved = False

    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.handle_login)
        self.ui.checkPassword.clicked.connect(self.check_pwd)

        app_manager.logout_signal.connect(self.handle_logout)

    def handle_login(self):
        login = self.ui.usernameEdit.text()
        password = self.ui.passwordEdit.text()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        user = authenticate_user(login, password)

        if user:
            self.session_was_saved = self.ui.checkBox.isChecked()
            if self.session_was_saved:
                save_user_session(user.id)

            app_manager.show_main_signal.emit(user.id, user.is_admin)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")


    def show_main_window(self, user_id, is_admin):
        self.hide()
        if self.main_window is None:
            self.main_window = MainWindow(user_id, is_admin=is_admin)
        else:
            self.main_window.update_user_data(user_id, is_admin=is_admin)

        self.main_window.show()

    def check_pwd(self):
        if self.ui.checkPassword.isChecked():
            self.ui.passwordEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

    def show_window(self):
        if hasattr(self, 'main_window') and self.main_window and self.main_window.isVisible():
            return
        self.show()
        self.raise_()
        self.activateWindow()
        self.ui.usernameEdit.setFocus()

    def handle_logout(self):
        self.ui.usernameEdit.clear()
        self.ui.passwordEdit.clear()
        self.ui.checkPassword.setChecked(False)
        self.ui.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        if not self.session_was_saved:
            self.show()