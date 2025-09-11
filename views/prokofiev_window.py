from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
                               QHeaderView, QGroupBox, QTextEdit)
from PySide6.QtCore import Qt

from analytics.ryab import calculate, normalize_data, get_data
from controllers.data_crud import get_all_data_dataframe
from libs.database import get_db
from controllers.analysis_crud import save_analysis_result
from analytics.corel_matrix import get_correl_matrix

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Аналитический модуль - Метод Рябцева")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Кнопка расчета
        calc_btn = QPushButton("Рассчитать интегральный показатель")
        calc_btn.clicked.connect(self.calculate_integral)
        calc_btn.setStyleSheet("background: #2196F3; color: white; padding: 10px;")
        layout.addWidget(calc_btn)

        # Группа для результатов
        results_group = QGroupBox("Результаты расчета")
        results_layout = QVBoxLayout()

        # Таблица с интегральными показателями
        self.integral_table = QTableWidget()
        self.integral_table.setColumnCount(2)
        self.integral_table.setHorizontalHeaderLabels(["Год", "Интегральный показатель"])
        self.integral_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_layout.addWidget(QLabel("Интегральные показатели качества:"))
        results_layout.addWidget(self.integral_table)

        # Таблица с весами
        self.weights_table = QTableWidget()
        self.weights_table.setColumnCount(2)
        self.weights_table.setHorizontalHeaderLabels(["Показатель", "Вес"])
        self.weights_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_layout.addWidget(QLabel("Веса показателей:"))
        results_layout.addWidget(self.weights_table)

        # Область для интерпретации
        self.interpretation_text = QTextEdit()
        self.interpretation_text.setReadOnly(True)
        self.interpretation_text.setMaximumHeight(150)
        results_layout.addWidget(QLabel("Интерпретация результатов:"))
        results_layout.addWidget(self.interpretation_text)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        self.setLayout(layout)
        self.setWindowTitle("Рассчет ср./сут. интервала с помощью метода Прокофьева")
        self.resize(800, 800)


    def calculate_integral(self):
        """Расчет интегрального показателя"""
        try:
            db = next(get_db())

            # Получаем все годы из базы
            from controllers.data_crud import get_all_data
            data = get_all_data(db)
            years = [record.year for record in data]
            if not years:
                QMessageBox.warning(self, "Ошибка", "Нет данных для анализа!")
                return

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка расчета: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def display_results(self, results, weights):
        pass

