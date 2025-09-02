from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QGroupBox, QTextEdit
)
from PySide6.QtCore import Qt
from libs.database import get_db
from analytics.ryabtsev import RyabtsevMethod
from controllers.analysis_crud import save_analysis_result
from controllers.data_crud import get_all_data

# для графика
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ryabtsev = RyabtsevMethod()
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

        # Группа результатов
        results_group = QGroupBox("Результаты расчета")
        results_layout = QVBoxLayout()

        # Таблица интегральных показателей
        self.integral_table = QTableWidget()
        self.integral_table.setColumnCount(2)
        self.integral_table.setHorizontalHeaderLabels(["Год", "Интегральный показатель"])
        self.integral_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_layout.addWidget(QLabel("Интегральные показатели качества:"))
        results_layout.addWidget(self.integral_table)

        # Таблица весов
        self.weights_table = QTableWidget()
        self.weights_table.setColumnCount(2)
        self.weights_table.setHorizontalHeaderLabels(["Показатель", "Вес"])
        self.weights_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        results_layout.addWidget(QLabel("Веса показателей:"))
        results_layout.addWidget(self.weights_table)

        # Интерпретация
        self.interpretation_text = QTextEdit()
        self.interpretation_text.setReadOnly(True)
        self.interpretation_text.setMaximumHeight(150)
        results_layout.addWidget(QLabel("Интерпретация результатов:"))
        results_layout.addWidget(self.interpretation_text)

        # График
        self.figure = Figure(figsize=(6, 3))
        self.canvas = FigureCanvas(self.figure)
        results_layout.addWidget(QLabel("График динамики качества:"))
        results_layout.addWidget(self.canvas)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        self.setLayout(layout)
        self.setWindowTitle("Аналитика МЦК - Метод Рябцева")
        self.resize(900, 900)

    def calculate_integral(self):
        """Запуск расчета"""
        try:
            db = next(get_db())
            data = get_all_data(db)
            years = [record.year for record in data]

            if not years:
                QMessageBox.warning(self, "Ошибка", "Нет данных для анализа!")
                return

            results, weights = self.ryabtsev.calculate_integral_index(db, years)

            if not results:
                QMessageBox.warning(self, "Ошибка", "Не удалось рассчитать показатели!")
                return

            # сохраняем в БД
            for year, value in results.items():
                save_analysis_result(db, year, value)

            # отображаем
            self.display_results(results, weights)
            self.display_interpretation(weights)
            self.display_chart(results)

            QMessageBox.information(self, "Успех", "Расчет завершен!")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка расчета: {str(e)}")

    def display_results(self, results, weights):
        """Таблицы"""
        # интегральные показатели
        self.integral_table.setRowCount(len(results))
        for row, (year, value) in enumerate(sorted(results.items())):
            self.integral_table.setItem(row, 0, QTableWidgetItem(str(year)))
            self.integral_table.setItem(row, 1, QTableWidgetItem(f"{value:.3f}"))

        # веса
        self.weights_table.setRowCount(len(weights))
        for row, (indicator, weight) in enumerate(sorted(weights.items(), key=lambda x: x[1], reverse=True)):
            name = self.ryabtsev.get_indicator_name(indicator)
            self.weights_table.setItem(row, 0, QTableWidgetItem(name))
            self.weights_table.setItem(row, 1, QTableWidgetItem(f"{weight:.4f}"))

    def display_interpretation(self, weights):
        if not weights:
            self.interpretation_text.setPlainText("Недостаточно данных для анализа")
            return
        self.interpretation_text.setPlainText(self.ryabtsev.get_interpretation(weights))

    def display_chart(self, results):
        """График динамики"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        years = sorted(results.keys())
        values = [results[y] for y in years]

        ax.plot(years, values, marker="o", linewidth=2, color="blue")
        ax.set_title("Динамика интегрального показателя (Рябцев)")
        ax.set_xlabel("Год")
        ax.set_ylabel("Индекс качества")
        ax.grid(True)

        self.canvas.draw()
