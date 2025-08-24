from PySide6.QtCore import QObject, Signal


class AppManager(QObject):
    # Сигналы для переключения между окнами авторизации/регистрации
    show_auth_signal = Signal()
    show_reg_signal = Signal()

    # Сигнал для выхода (из главного окна обратно к авторизации)
    logout_signal = Signal()

    def __init__(self):
        super().__init__()

app_manager = AppManager()