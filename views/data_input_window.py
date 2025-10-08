from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView,
    QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt
from libs.database import get_db
from controllers.data_crud import create_mck_data, get_all_data, delete_data, update_data


class DataInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Scroll Area
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Ввод данных МЦК")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        scroll_layout.addWidget(title)

        # Сетка для ввода
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Поля ввода
        self.inputs = {}
        fields = [
            ('year', 'Год:', str(datetime.today().year), 0, 0),
            ('failures_1', 'Отказы 1 кат.:', '0', 0, 1),
            ('failures_2', 'Отказы 2 кат.:', '0', 0, 2),
            ('failures_3', 'Отказы 3 кат.:', '0', 0, 3),

            ('train_losses', 'Поездопотери:', '0.0', 1, 0),
            ('investments', 'Кап. вложения:', '0.0', 1, 1),
            ('passengers_daily', 'Пассажиры (сут.):', '0', 1, 2),
            ('tech_failures', 'Тех. отказы:', '0', 1, 3),

            ('fare_cost', 'Стоимость проезда:', '0.0', 2, 0),
            ('interval', 'Интервал движения:', '0.0', 2, 1),
        ]

        for field_name, label_text, placeholder, row, col in fields:
            grid_layout.addWidget(QLabel(label_text), row, col * 2)
            self.inputs[field_name] = QLineEdit()
            self.inputs[field_name].setPlaceholderText(placeholder)
            grid_layout.addWidget(self.inputs[field_name], row, col * 2 + 1)

        scroll_layout.addLayout(grid_layout)

        # Кнопка добавления
        add_btn = QPushButton("Добавить данные")
        add_btn.clicked.connect(self.add_data)
        add_btn.setStyleSheet("background: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        scroll_layout.addWidget(add_btn)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        headers = [
            "Год", "Отказы 1", "Отказы 2", "Отказы 3", "Поездопотери",
            "Кап. вложения", "Пассажиры", "Тех. отказы", "Стоимость", "Интервал", "Действия"
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Включаем редактирование таблицы
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.table.cellChanged.connect(self.on_cell_changed)

        scroll_layout.addWidget(self.table)

        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)

        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.setWindowTitle("Ввод данных МЦК")
        self.resize(1200, 700)

        # Флаг для предотвращения рекурсивных вызовов
        self._updating_cell = False

    def on_cell_changed(self, row, column):
        """Обработчик изменения ячейки таблицы"""
        if self._updating_cell:
            return

        try:
            self._updating_cell = True

            # Получаем год из первого столбца
            year_item = self.table.item(row, 0)
            if not year_item:
                return

            year = int(year_item.text())

            # Получаем новое значение
            item = self.table.item(row, column)
            if not item:
                return

            new_value = item.text()

            # Определяем поле для обновления
            field_map = {
                1: 'failures_1',
                2: 'failures_2',
                3: 'failures_3',
                4: 'train_losses',
                5: 'investments',
                6: 'passengers_daily',
                7: 'tech_failures',
                8: 'fare_cost',
                9: 'interval'
            }

            field_name = field_map.get(column)
            if not field_name:
                return

            # Преобразуем значение к правильному типу
            if field_name in ['failures_1', 'failures_2', 'failures_3', 'passengers_daily', 'tech_failures']:
                value = int(new_value)
            elif field_name in ['train_losses', 'investments', 'fare_cost', 'interval']:
                value = float(new_value)
            else:
                value = new_value

            # Обновляем данные в БД
            db = next(get_db())
            update_data(db, year, **{field_name: value})

            # Обновляем форматирование в таблице
            if field_name in ['train_losses', 'investments', 'fare_cost']:
                item.setText(f"{value:.2f}")
            elif field_name == 'interval':
                item.setText(f"{value:.4f}")

            QMessageBox.information(self, "Успех", f"Данные за {year} год обновлены!")

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректное значение: {str(e)}")
            # Перезагружаем данные для восстановления исходных значений
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка обновления: {str(e)}")
            self.load_data()
        finally:
            self._updating_cell = False

    def add_data(self):
        """Добавление новых данных"""
        try:
            data = {
                'year': int(self.inputs['year'].text()),
                'failures_1': int(self.inputs['failures_1'].text()),
                'failures_2': int(self.inputs['failures_2'].text()),
                'failures_3': int(self.inputs['failures_3'].text()),
                'train_losses': float(self.inputs['train_losses'].text()),
                'investments': float(self.inputs['investments'].text()),
                'passengers_daily': int(self.inputs['passengers_daily'].text()),
                'tech_failures': int(self.inputs['tech_failures'].text()),
                'fare_cost': float(self.inputs['fare_cost'].text()),
                'interval': float(self.inputs['interval'].text())
            }

            db = next(get_db())
            create_mck_data(db, **data)

            self.clear_inputs()
            self.load_data()
            QMessageBox.information(self, "Успех", "Данные добавлены!")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Проверьте правильность введенных данных!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка добавления: {str(e)}")

    def clear_inputs(self):
        for input_field in self.inputs.values():
            input_field.clear()

    def load_data(self):
        """Загрузка данных в таблицу"""
        # Временно отключаем обработчик изменений
        self.table.cellChanged.disconnect()

        try:
            db = next(get_db())
            data = get_all_data(db)
            self.table.setRowCount(len(data))

            for row, record in enumerate(data):
                self.table.setItem(row, 0, QTableWidgetItem(str(record.year)))
                self.table.setItem(row, 1, QTableWidgetItem(str(record.failures_1)))
                self.table.setItem(row, 2, QTableWidgetItem(str(record.failures_2)))
                self.table.setItem(row, 3, QTableWidgetItem(str(record.failures_3)))
                self.table.setItem(row, 4, QTableWidgetItem(f"{record.train_losses:.2f}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"{record.investments:.2f}"))
                self.table.setItem(row, 6, QTableWidgetItem(str(record.passengers_daily)))
                self.table.setItem(row, 7, QTableWidgetItem(str(record.tech_failures)))
                self.table.setItem(row, 8, QTableWidgetItem(f"{record.fare_cost:.2f}"))
                self.table.setItem(row, 9, QTableWidgetItem(f"{record.interval:.4f}"))

                # Кнопка удаления
                delete_btn = QPushButton("Удалить")
                delete_btn.setStyleSheet("background: #f44336; color: white;")
                delete_btn.clicked.connect(lambda checked, y=record.year: self.delete_record(y))
                self.table.setCellWidget(row, 10, delete_btn)

        finally:
            # Восстанавливаем обработчик
            self.table.cellChanged.connect(self.on_cell_changed)

    def delete_record(self, year):
        try:
            db = next(get_db())
            delete_data(db, year)
            self.load_data()
            QMessageBox.information(self, "Успех", f"Данные за {year} год удалены!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка удаления: {str(e)}")