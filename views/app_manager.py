from PySide6.QtCore import QObject, Signal


class AppManager(QObject):
    show_main_signal = Signal(int, bool)  # user_id, is_admin
    logout_signal = Signal(bool) # сохранена ли авторизация? True or False

    def __init__(self):
        super().__init__()


app_manager = AppManager()