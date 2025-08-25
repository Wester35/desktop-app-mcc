from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QApplication
from ui.ui_main import Ui_MainWindow
from views.app_manager import app_manager
from controllers.crud import delete_user_session
from views.register_window import Register


class MainWindow(QWidget):
    def __init__(self,user_id, is_admin):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_id = user_id
        self.is_admin = is_admin

        self.connect_signals()

        self.setWindowIcon(QPixmap("ui/resources/app_icon.png"))

    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.show_register_window)
        self.ui.pushButton_2.clicked.connect(self.logout)

    def update_user_data(self, user_id, is_admin):
        self.user_id = user_id
        self.is_admin = is_admin

    def show_register_window(self):
        self.register_window = Register()
        self.register_window.show()

    def logout(self):
        delete_user_session()
        app_manager.logout_signal.emit()
        self.close()

    def handle_logout(self):
        delete_user_session()
        self.close()

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()