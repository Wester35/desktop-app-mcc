from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit
# from controllers.crud import authenticate_user, save_user_session
from ui.ui_main import Ui_MainWindow
from views.app_manager import app_manager
from controllers.crud import delete_user_session

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_signals()

        self.setWindowIcon(QPixmap("ui/resources/app_icon.png"))

    def connect_signals(self):
        app_manager.logout_signal.connect(self.handle_logout)

    def update_user_data(self, user_id):
        self.user_id = user_id

    def logout(self):
        delete_user_session()
        app_manager.logout_signal.emit()

    def handle_logout(self):
        self.close()

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        # При закрытии главного окна тоже отправляем сигнал выхода
        app_manager.logout_signal.emit()
        event.accept()