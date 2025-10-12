from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QLabel, QMessageBox, QLineEdit, QApplication,
                               QMainWindow, QDialog, QHBoxLayout, QVBoxLayout,
                               QTextEdit, QPushButton)

from analytics.graphics import plot_regression_diagnostics
from ui.main_window_ui import Ui_MainWindow
from views.analytics_window import AnalyticsWindow
from views.app_manager import app_manager
from controllers.crud import delete_user_session, get_user_data
from views.data_input_window import DataInputWindow
from views.integral_regression_window import IntegralRegressionWindow
from views.interval_regression_window import IntervalRegressionWindow
from views.profile_window import ProfileWindow
from views.prokofiev_window import ProkofievWindow
from views.register_window import Register


class MainWindow(QMainWindow):
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
        self.profile_window = None
        self.integral_window = None
        self.interval_window = None
        self.setWindowIcon(QPixmap("ui/resources/app_icon.png"))
        self.setup_ui_based_on_permissions()

    def setup_ui_based_on_permissions(self):
        if not self.is_admin:
            self.ui.pushButton.hide()
        else:
            self.ui.pushButton.show()


    def set_session_saved(self, saved):
        self.session_was_saved = saved

    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.show_register_window)
        self.ui.pushButton_2.clicked.connect(self.logout)

        self.ui.data_input_btn.clicked.connect(self.open_data_input)
        self.ui.analytics_btn.clicked.connect(self.open_analytics)

        self.ui.prokofiev_button.clicked.connect(self.open_prokofiev_window)
        self.ui.profile_btn.clicked.connect(self.open_profile_window)
        self.ui.integral_window.clicked.connect(self.open_integral_window)
        self.ui.interval_window.clicked.connect(self.open_interval_window)
        self.ui.integral_charts.clicked.connect(self.open_integral_charts)
        self.ui.interval_charts.clicked.connect(self.open_interval_charts)
        self.ui.menu.aboutToShow.connect(self.show_user_guide)


    def open_profile_window(self):
        if self.profile_window is None:
            self.profile_window = ProfileWindow(self.user_id, self.is_admin)
        self.profile_window.show()

    def open_integral_charts(self):
        try:
            plot_regression_diagnostics("integral")
        except FileNotFoundError as e:
            QMessageBox.warning(self, "Ошибка", f"Не выполнены предыдущие шаги!\n {e}")

    def open_interval_charts(self):
        try:
            plot_regression_diagnostics("interval")
        except FileNotFoundError as e:
            QMessageBox.warning(self, "Ошибка", f"Не выполнены предыдущие шаги!\n {e}")

    def open_integral_window(self):
        if self.integral_window is None:
            self.integral_window = IntegralRegressionWindow()
        self.integral_window.show()

    def open_interval_window(self):
        if self.interval_window is None:
            self.interval_window = IntervalRegressionWindow()
        self.interval_window.show()

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
        try:
            data=get_user_data(self.user_id)
            self.register_window = Register(data['login'])
            print(data['login'])
            self.register_window.show()
        except Exception:
            print("Ошибка БД")

    def logout(self):
        self.ui.pushButton.hide()
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

    def show_user_guide(self):
        """Показывает справку по использованию программы"""
        help_text = (
            "РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ — DesktopAppMCC\n"
            "=========================================\n\n"
            "🔑 Авторизация\n"
            "--------------\n"
            "После установки и запуска приложения в окне авторизации требуется войти под учетными данными:\n"
            "  • Логин: admin\n"
            "  • Пароль: admin\n\n"
            "После входа откроется главное окно с кнопками, открывающими различные разделы системы.\n"
            "В окне «Профиль» можно изменить пароль и просмотреть данные учетной записи.\n\n"
            "⚙️ Порядок работы при вычислениях\n"
            "--------------------------------\n"
            "1. Ввод данных.\n"
            "2. Расчет интегральных показателей.\n"
            "3. Построение интегральной модели.\n"
            "4. Построение интервальной модели.\n\n"
            "📊 Предварительный анализ (ДО построения моделей)\n"
            "------------------------------------------------\n"
            "На начальном этапе необходимо осуществить вычисление матрицы корреляции.\n"
            "Далее отобрать те значения парных коэффициентов корреляции между ФАКТОРАМИ, которые больше 0.6.\n"
            "Далее необходимо определить, какой из них не будет включен в модель.\n"
            "Смотрим, у кого из них сильнее влияние на результативный показатель\n"
            "(тоже по парному коэффициенту корреляции, но уже МЕЖДУ ФАКТОРОМ И ИГРЕКОМ).\n"
            "Соответственно, в модель будет включен тот фактор, у кого корреляция с игреком больше.\n"
            "Эта процедура осуществляется в ручном режиме самим исследователем.\n"
            "После этого можно перейти к расчетам моделей.\n"
            "\n\n"
            "🧮 Инструкция по построению моделей\n"
            "-----------------------------------\n"
            "• Откройте соответствующее окно модели (Интегральная / Интервальная).\n"
            "• Выберите нужные факторы галочками или используйте автоматический режим.\n"
            "• Нажмите «Построить регрессию» для выполнения расчета.\n"
            "• После расчета программа выведет уравнение регрессии, коэффициенты и статистические показатели:\n"
            "  - R² — коэффициент детерминации (доля объясненной вариации).\n"
            "  - Fфакт и Fкр — проверка статистической значимости модели.\n"
            "  - t-значения — проверка значимости отдельных факторов.\n\n"
            "📈 Просмотр графиков\n"
            "--------------------\n"
            "В разделе «Графики» доступны результаты визуализации регрессионных моделей:\n"
            "  • Интегральные графики.\n"
            "  • Среднесуточные графики.\n"
            "Если отображается сообщение «Не выполнены предыдущие шаги» — выполните расчеты моделей заново.\n\n"
            "🧾 Прогнозирование\n"
            "------------------\n"
            "Откройте окно «Прогнозы», чтобы просмотреть результаты моделей. Сами уравнения сохраняются скрытно.\n\n"
            "👥 Работа с пользователями\n"
            "--------------------------\n"
            "• Новые пользователи регистрируются через кнопку «Регистрация».\n"
            "• Главный администратор (логин admin) может добавлять других администраторов.\n"
            "• Остальные администраторы могут регистрировать обычных пользователей.\n\n"
            "🚪 Выход из системы\n"
            "-------------------\n"
            "• Кнопка «Выход» завершает текущую сессию и при необходимости удаляет сохранённые данные входа.\n"
            "• При следующем запуске потребуется повторная авторизация.\n\n"
            "----------------------------------------------\n"
            "Приложение: DesktopAppMCC\n"
            "Разработчик: Wester35\n"
            "Версия: 1.0\n"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Справка по программе")
        dialog.resize(800, 600)

        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(help_text)
        layout.addWidget(text_edit)

        # кнопка закрытия
        btn_layout = QHBoxLayout()
        ok_button = QPushButton("Закрыть")
        ok_button.clicked.connect(dialog.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(ok_button)
        layout.addLayout(btn_layout)

        dialog.exec()
