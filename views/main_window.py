from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox, QLineEdit, QApplication
from ui.ui_main import Ui_MainWindow
from views.analytics_window import AnalyticsWindow
from views.app_manager import app_manager
from controllers.crud import delete_user_session
from views.data_input_window import DataInputWindow
from views.prokofiev_window import ProkofievWindow
from views.register_window import Register


class MainWindow(QWidget):
    def __init__(self,user_id, is_admin):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_id = user_id
        self.is_admin = is_admin
        self.session_was_saved = False
        self.connect_signals()
        self.data_input_window = None
        self.prokofiev_window = None
        self.analytics_window = None
        self.setWindowIcon(QPixmap("ui/resources/app_icon.png"))

    def set_session_saved(self, saved):
        self.session_was_saved = saved

    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.show_register_window)
        self.ui.pushButton_2.clicked.connect(self.logout)
        #############################
        # Кнопка для ввода данных
        self.ui.data_input_btn.clicked.connect(self.open_data_input)
        # Кнопка для аналитики
        self.ui.analytics_btn.clicked.connect(self.open_analytics)

        self.ui.prokofiev_button.clicked.connect(self.open_prokofiev_window)

    def open_prokofiev_window(self):
        if self.prokofiev_window is None:
            self.prokofiev_window = ProkofievWindow()
        self.prokofiev_window.show()

    def open_data_input(self):
        """Открытие окна ввода данных"""
        if self.data_input_window is None:
            self.data_input_window = DataInputWindow()
        self.data_input_window.show()

    def open_analytics(self):
        """Открытие окна аналитики"""
        if self.analytics_window is None:
            self.analytics_window = AnalyticsWindow()
        self.analytics_window.show()

    def update_user_data(self, user_id, is_admin):
        self.user_id = user_id
        self.is_admin = is_admin

    def show_register_window(self):
        self.register_window = Register()
        self.register_window.show()

    def logout(self):
        delete_user_session()
        app_manager.logout_signal.emit(self.session_was_saved)
        self.close()

    def handle_logout(self):
        delete_user_session()
        self.close()

    def closeEvent(self, event):
        if self.session_was_saved:
            QApplication.quit()
        else:
            event.accept()