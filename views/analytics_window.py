from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
                               QHeaderView, QGroupBox, QTextEdit)
from PySide6.QtCore import Qt

from analytics.ryab import calculate, normalize_data, get_data
from controllers.data_crud import get_all_data_dataframe
from libs.database import get_db
from controllers.analysis_crud import save_analysis_result


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
        self.setWindowTitle("Аналитика МЦК - Метод Рябцева")
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

            data_for_normalize = get_data(db, years)


            results, weights = calculate(normalize_data(data_for_normalize))
            results = results['weighted_sum'].to_dict()
            weights = weights['correlation'].to_dict()
            if not results:
                QMessageBox.warning(self, "Ошибка", "Не удалось рассчитать показатели!")
                return


            # Сохраняем результаты
            for year, value in results.items():
                save_analysis_result(db, year, value)

            # Отображаем результаты
            self.display_results(results, weights)
            self.display_interpretation(weights)

            QMessageBox.information(self, "Успех", "Расчет завершен!")

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка расчета: {str(e)}")
            import traceback
            print(traceback.format_exc())  # Для детальной отладки

    def display_results(self, results, weights):
        """Отображение результатов в таблицах"""
        # Интегральные показатели
        self.integral_table.setRowCount(len(results))
        for row, (year, value) in enumerate(results.items()):
            self.integral_table.setItem(row, 0, QTableWidgetItem(str(year)))
            self.integral_table.setItem(row, 1, QTableWidgetItem(f"{value:.4f}"))

        # Веса показателей
        self.weights_table.setRowCount(len(weights))
        for row, (indicator, weight) in enumerate(weights.items()):
            self.weights_table.setItem(row, 0, QTableWidgetItem(self.get_indicator_name(indicator)))
            self.weights_table.setItem(row, 1, QTableWidgetItem(f"{weight:.4f}"))

    def display_interpretation(self, weights):
        """Отображение интерпретации результатов"""
        if not weights:
            return

        # Сортируем показатели по весу
        sorted_weights = sorted(weights.items(), key=lambda x: x[1], reverse=True)

        interpretation = "📊 АНАЛИЗ ВЛИЯНИЯ ПОКАЗАТЕЛЕЙ НА КАЧЕСТВО ОБСЛУЖИВАНИЯ:\n\n"

        interpretation += "🎯 НАИБОЛЬШЕЕ ВЛИЯНИЕ:\n"
        for indicator, weight in sorted_weights[:3]:
            interpretation += f"• {self.get_indicator_name(indicator)}: {weight:.1%}\n"

        interpretation += "\n⚡ РЕКОМЕНДАЦИИ:\n"
        interpretation += f"- Основное внимание уделите {self.get_indicator_name(sorted_weights[0][0])}\n"
        interpretation += f"- Второй по важности фактор: {self.get_indicator_name(sorted_weights[1][0])}\n"
        interpretation += f"- Также значимо: {self.get_indicator_name(sorted_weights[2][0])}\n"

        self.interpretation_text.setPlainText(interpretation)

    def get_indicator_name(self, key):
        """Получение читаемого названия показателя"""
        names = {
            'failures_1': 'Отказы 1 категории',
            'failures_2': 'Отказы 2 категории',
            'failures_3': 'Отказы 3 категории',
            'train_losses': 'Поездопотери',
            'investments': 'Капитальные вложения',
            'passengers_daily': 'Пассажиры (сут.)',
            'tech_failures': 'Технические отказы',
            'fare_cost': 'Стоимость проезда'
        }
        return names.get(key, key)