import pickle
from pathlib import Path

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
                               QHeaderView, QGroupBox, QTextEdit)
from PySide6.QtCore import Qt

from analytics.predict import calculate_final_predict
from analytics.ryab import calculate, normalize_data, get_data
from controllers.data_crud import get_all_data_dataframe
from libs.database import get_db
from controllers.analysis_crud import save_analysis_result
from analytics.corel_matrix import get_correl_matrix

class ProkofievWindow(QWidget):
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
        calc_btn = QPushButton("Рассчитать ср.сут. интервал")
        calc_btn.clicked.connect(self.calculate_equation)
        calc_btn.setStyleSheet("background: #2196F3; color: white; padding: 10px;")
        layout.addWidget(calc_btn)


        result_label = QLabel("Точечный прогноз среднесуточного интервала по модели: ")
        self.result_label = result_label
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(result_label)


        self.setLayout(layout)
        self.setWindowTitle("Рассчет ср./сут. интервала с помощью метода Прокофьева")
        self.resize(800, 200)


    def calculate_equation(self):
        """Расчет интегрального показателя"""
        try:
            db = next(get_db())
            with open(Path(__file__).parent.parent.absolute() / 'data/interval.pkl', 'rb') as file:
                loaded_dict = pickle.load(file)
            self.result_label.setText("Точечный прогноз среднесуточного интервала по модели: " +
                                      str(calculate_final_predict(db, loaded_dict)))

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка расчета: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def display_results(self, results, weights):
        pass

