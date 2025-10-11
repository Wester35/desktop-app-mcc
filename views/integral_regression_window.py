import pickle
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QCheckBox, QTextEdit, QHBoxLayout, QMessageBox
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
        self.years = [record.year for record in data]
        self.checkboxes = {}
        self.cb_layout = None
        self.setup_ui()
        self.load_corr_table()

    def setup_ui(self):
        self.layout_main = QVBoxLayout()

        title = QLabel("Матрица коллинеарности (интегральный показатель)")
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

    def show_warning(self, message: str):
        """Показать окно-предупреждение"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Предупреждение")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def load_corr_table(self):
        """Загружаем и фильтруем матрицу коллинеарности"""
        try:
            corr_matrix = get_correl_matrix(self.db, self.years)
        except Exception:
            self.show_warning("⚠️ Не удалось получить данные корреляции. Возможно, не выполнены предыдущие шаги.")
            self.corr_table.clear()
            return

        if "integrated_index" not in corr_matrix.index:
            self.show_warning("⚠️ В данных отсутствует показатель 'integrated_index'. Проверьте этап расчёта данных.")
            self.corr_table.clear()
            return

        # Берем строку зависимости по 'integrated_index'
        corr_with_y = corr_matrix.loc["integrated_index"].drop("integrated_index")

        # фильтруем факторы по корреляции >= 0.18
        kept_factors = corr_with_y[abs(corr_with_y) >= 0.18].index.tolist()

        # гарантируем наличие 'integrated_index' (ставим на первое место)
        if "integrated_index" not in kept_factors:
            kept_factors.insert(0, "integrated_index")
        else:
            kept_factors.remove("integrated_index")
            kept_factors.insert(0, "integrated_index")

        if not kept_factors:
            self.show_warning("⚠️ Нет факторов с корреляцией ≥ 0.18. Необходимо выполнить предыдущие шаги анализа.")
            self.corr_table.clear()
            return

        # формируем подматрицу
        filtered_matrix = corr_matrix.loc[kept_factors, kept_factors]

        # вывод таблицы
        self.corr_table.setRowCount(len(filtered_matrix))
        self.corr_table.setColumnCount(len(filtered_matrix))
        self.corr_table.setHorizontalHeaderLabels(filtered_matrix.columns.tolist())
        self.corr_table.setVerticalHeaderLabels(filtered_matrix.index.tolist())

        for i, row_factor in enumerate(filtered_matrix.index):
            for j, col_factor in enumerate(filtered_matrix.columns):
                value = filtered_matrix.loc[row_factor, col_factor]
                item = QTableWidgetItem(f"{value:.3f}")
                item.setTextAlignment(Qt.AlignCenter)
                self.corr_table.setItem(i, j, item)

        # пересоздаём чекбоксы (кроме integrated_index)
        for i in reversed(range(self.cb_layout.count())):
            widget = self.cb_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.checkboxes.clear()

        for factor in kept_factors:
            if factor == "integrated_index":
                continue  # без чекбокса
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

        # сохраняем результат
        save_path = Path.home() / "AppData" / "Local" / "DesktopAppMCC" / 'data/integral.pkl'
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as file:
            pickle.dump(result, file)

        # вывод результата
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
