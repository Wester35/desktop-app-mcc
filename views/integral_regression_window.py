import pickle
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QCheckBox, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import Qt
import pandas as pd

from libs.database import get_db
from controllers.data_crud import get_all_data
from analytics.corel_matrix import get_correl_matrix
from analytics.equations import build_integral_model


class IntegralRegressionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = next(get_db())
        data = get_all_data(self.db)
        years = [record.year for record in data]
        self.years = years
        self.checkboxes = {}
        self.cb_layout = None
        self.setup_ui()
        self.load_corr_table()

    def setup_ui(self):
        self.layout_main = QVBoxLayout()

        title = QLabel("Регрессия: интегральный показатель")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        self.layout_main.addWidget(title)

        # Таблица корреляций
        self.corr_table = QTableWidget()
        self.layout_main.addWidget(self.corr_table)

        # контейнер для чекбоксов
        self.cb_layout = QHBoxLayout()
        self.layout_main.addLayout(self.cb_layout)

        # Флажок авто-шаг
        self.auto_step_checkbox = QCheckBox("Автоматическое пошаговое исключение факторов")
        self.auto_step_checkbox.setChecked(True)
        self.layout_main.addWidget(self.auto_step_checkbox)

        # Кнопка построения
        run_btn = QPushButton("Построить регрессию")
        run_btn.clicked.connect(self.run_regression)
        self.layout_main.addWidget(run_btn)

        # Вывод результатов
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.layout_main.addWidget(self.result_output)

        self.setLayout(self.layout_main)
        self.resize(1000, 600)
        self.setWindowTitle("Регрессия интегрального показателя")

    def load_corr_table(self):
        """Загружаем корреляции с y, убираем факторы < 0.18 и отмечаем мультиколлинеарность"""
        corr_matrix = get_correl_matrix(self.db, self.years)
        corr_with_y = corr_matrix.loc["integrated_index"].drop("integrated_index")

        # фильтрация по 0.18
        corr_with_y = corr_with_y[corr_with_y.abs() >= 0.18]

        # словарь статусов
        statuses = {f: "Ок" for f in corr_with_y.index}

        # проверяем пары факторов на мультиколлинеарность
        factors = list(corr_with_y.index)
        for i in range(len(factors)):
            for j in range(i + 1, len(factors)):
                f1, f2 = factors[i], factors[j]
                corr_val = corr_matrix.loc[f1, f2]

                if abs(corr_val) > 0.6:
                    if abs(corr_with_y[f1]) >= abs(corr_with_y[f2]):
                        statuses[f1] = "Мульти: сильнее"
                        statuses[f2] = "Мульти: слабее"
                    else:
                        statuses[f1] = "Мульти: слабее"
                        statuses[f2] = "Мульти: сильнее"

        # строим таблицу
        self.corr_table.setColumnCount(3)
        self.corr_table.setRowCount(len(corr_with_y))
        self.corr_table.setHorizontalHeaderLabels(["Фактор", "Корреляция с y", "Статус"])

        for i, (factor, value) in enumerate(corr_with_y.items()):
            self.corr_table.setItem(i, 0, QTableWidgetItem(str(factor)))
            self.corr_table.setItem(i, 1, QTableWidgetItem(f"{value:.4f}"))
            self.corr_table.setItem(i, 2, QTableWidgetItem(statuses[factor]))

        # пересоздаём чекбоксы
        # сначала убираем старые
        for i in reversed(range(self.cb_layout.count())):
            widget = self.cb_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.checkboxes.clear()

        # добавляем новые чекбоксы для оставшихся факторов
        for factor in corr_with_y.index:
            cb = QCheckBox(factor)
            self.checkboxes[factor] = cb
            self.cb_layout.addWidget(cb)

    def run_regression(self):
        """Запускаем регрессию по выбранным пользователем факторам"""
        selected = [f for f, cb in self.checkboxes.items() if cb.isChecked()]

        if not selected:
            self.result_output.setPlainText("⚠️ Не выбраны факторы!")
            return
        iterative = self.auto_step_checkbox.isChecked()

        result = build_integral_model(self.db, self.years, selected, iterative=iterative)

        with open(Path.home() / "AppData" / "Local" / "DesktopAppMCC" / 'data/integral.pkl', 'wb') as file:
            pickle.dump(result, file)

        output_lines = []
        output_lines.append("=== Результат регрессии ===")
        output_lines.append(f"Факторы: {', '.join(selected)}")
        output_lines.append("")
        output_lines.append("Уравнение:")
        terms = []
        for k, v in result["equation"].items():
            if k == "const":
                const_val = round(v, 6)
            else:
                coef = round(v, 6)
                sign = "+" if coef >= 0 else "-"
                terms.append(f" {sign} {abs(coef)}*{k}")
        output_lines.append(f"y = {const_val}" + "".join(terms))
        output_lines.append(str(result["equation"]))
        output_lines.append("")
        output_lines.append(f"R² = {result['r2']:.4f}")
        output_lines.append(f"Fфакт = {result['f_fact']:.4f}, Fкр = {result['f_crit']}")
        output_lines.append("")
        output_lines.append("Коэффициенты и t-значения:")
        for k, coef in result["equation"].items():
            t_val = result["t_values"].get(k, None)
            output_lines.append(
                f"  {k}: {coef:.6f}, t = {t_val:.6f}" if t_val else f"  {k}: {coef:.6f}"
            )

        self.result_output.setPlainText("\n".join(output_lines))
