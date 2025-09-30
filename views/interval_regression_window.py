import pickle
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QCheckBox, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import Qt
import pandas as pd

from analytics.corel_matrix import get_second_correl_matrix
from analytics.equations import build_interval_model
from controllers.data_crud import get_all_data
from libs.database import get_db


class IntervalRegressionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = next(get_db())
        data = get_all_data(self.db)
        years = [record.year for record in data]
        self.years = years
        self.selected_factors = []
        self.setup_ui()
        self.load_corr_table()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Регрессия: среднесуточный интервал")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Таблица корреляций
        self.corr_table = QTableWidget()
        layout.addWidget(self.corr_table)

        # Блок чекбоксов
        self.checkboxes = {}
        factors = [
            "failures_1", "failures_2", "failures_3",
            "train_losses", "investments", "passengers_daily",
            "tech_failures", "fare_cost"
        ]

        cb_layout = QHBoxLayout()
        for factor in factors:
            cb = QCheckBox(factor)
            self.checkboxes[factor] = cb
            cb_layout.addWidget(cb)
        layout.addLayout(cb_layout)
        self.auto_step_checkbox = QCheckBox("Автоматическое пошаговое исключение факторов")
        self.auto_step_checkbox.setChecked(True)  # по умолчанию включено
        layout.addWidget(self.auto_step_checkbox)

        # Кнопка построения
        run_btn = QPushButton("Построить регрессию")
        run_btn.clicked.connect(self.run_regression)
        layout.addWidget(run_btn)

        # Вывод результатов
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.setLayout(layout)
        self.resize(1000, 600)
        self.setWindowTitle("Регрессия интервала")

    def load_corr_table(self):
        """Загружаем таблицу корреляций (только строка interval)"""
        corr_matrix = get_second_correl_matrix(self.db, self.years)
        row = corr_matrix.loc["interval"].drop("interval")
        df = pd.DataFrame(row)

        self.corr_table.setColumnCount(2)
        self.corr_table.setRowCount(len(df))
        self.corr_table.setHorizontalHeaderLabels(["Фактор", "Корреляция с y"])

        for i, (factor, value) in enumerate(df.itertuples()):
            self.corr_table.setItem(i, 0, QTableWidgetItem(str(factor)))
            self.corr_table.setItem(i, 1, QTableWidgetItem(f"{value:.4f}"))

    def run_regression(self):
        """Запускаем регрессию по выбранным пользователем факторам"""
        selected = [f for f, cb in self.checkboxes.items() if cb.isChecked()]

        if not selected:
            self.result_output.setPlainText("⚠️ Не выбраны факторы!")
            return
        iterative = self.auto_step_checkbox.isChecked()

        result = build_interval_model(self.db, self.years, selected, iterative=iterative)

        with open(Path(__file__).parent.parent.absolute() / 'data/interval.pkl', 'wb') as file:
            pickle.dump(result, file)

        output_lines = []
        output_lines.append("=== Результат регрессии ===")
        output_lines.append(f"Факторы: {', '.join(selected)}")
        output_lines.append("")
        output_lines.append("Уравнение:")
        terms = []
        for k, v in result["equation"].items():
            if k == "const":
                tyt = round(v, 6)
            else:
                coef = round(v, 6)
                sign = "+" if coef >= 0 else "-"
                terms.append(f" {sign} {abs(coef)}*{k}")
        output_lines.append(f"y = {round(tyt, 6)}" + "".join(terms))
        output_lines.append(str(result["equation"]))
        output_lines.append("")
        output_lines.append(f"R² = {result['r2']:.4f}")
        output_lines.append(f"Fфакт = {result['f_fact']:.4f}, Fкр = {result['f_crit']}")
        output_lines.append("")
        output_lines.append("Коэффициенты и t-значения:")
        for k, coef in result["equation"].items():
            t_val = result["t_values"].get(k, None)
            output_lines.append(f"  {k}: {coef:.6f}, t = {t_val:.6f}" if t_val else f"  {k}: {coef:.6f}")

        self.result_output.setPlainText("\n".join(output_lines))
