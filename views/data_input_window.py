from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QGridLayout
)
from PySide6.QtCore import Qt
from libs.database import get_db
from controllers.data_crud import create_mck_data, get_all_data, delete_data


class DataInputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Ввод данных МЦК")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Сетка для полей ввода
        grid_layout = QGridLayout()
        self.inputs = {}

        # Первая строка
        grid_layout.addWidget(QLabel("Год:"), 0, 0)
        self.inputs['year'] = QLineEdit()
        self.inputs['year'].setPlaceholderText("2024")
        grid_layout.addWidget(self.inputs['year'], 0, 1)

        grid_layout.addWidget(QLabel("Отказы 1 кат.:"), 0, 2)
        self.inputs['failures_1'] = QLineEdit()
        self.inputs['failures_1'].setPlaceholderText("0")
        grid_layout.addWidget(self.inputs['failures_1'], 0, 3)

        grid_layout.addWidget(QLabel("Отказы 2 кат.:"), 0, 4)
        self.inputs['failures_2'] = QLineEdit()
        self.inputs['failures_2'].setPlaceholderText("0")
        grid_layout.addWidget(self.inputs['failures_2'], 0, 5)

        # Вторая строка
        grid_layout.addWidget(QLabel("Отказы 3 кат.:"), 1, 0)
        self.inputs['failures_3'] = QLineEdit()
        self.inputs['failures_3'].setPlaceholderText("0")
        grid_layout.addWidget(self.inputs['failures_3'], 1, 1)

        grid_layout.addWidget(QLabel("Поездопотери:"), 1, 2)
        self.inputs['train_losses'] = QLineEdit()
        self.inputs['train_losses'].setPlaceholderText("0.0")
        grid_layout.addWidget(self.inputs['train_losses'], 1, 3)

        grid_layout.addWidget(QLabel("Кап. вложения:"), 1, 4)
        self.inputs['investments'] = QLineEdit()
        self.inputs['investments'].setPlaceholderText("0.0")
        grid_layout.addWidget(self.inputs['investments'], 1, 5)

        # Третья строка
        grid_layout.addWidget(QLabel("Пассажиры (сут.):"), 2, 0)
        self.inputs['passengers_daily'] = QLineEdit()
        self.inputs['passengers_daily'].setPlaceholderText("0")
        grid_layout.addWidget(self.inputs['passengers_daily'], 2, 1)

        grid_layout.addWidget(QLabel("Тех. отказы:"), 2, 2)
        self.inputs['tech_failures'] = QLineEdit()
        self.inputs['tech_failures'].setPlaceholderText("0")
        grid_layout.addWidget(self.inputs['tech_failures'], 2, 3)

        grid_layout.addWidget(QLabel("Стоимость проезда:"), 2, 4)
        self.inputs['fare_cost'] = QLineEdit()
        self.inputs['fare_cost'].setPlaceholderText("0.0")
        grid_layout.addWidget(self.inputs['fare_cost'], 2, 5)

        # Четвертая строка (новое поле)
        grid_layout.addWidget(QLabel("Интервал движения (мин):"), 3, 0)
        self.inputs['interval'] = QLineEdit()
        self.inputs['interval'].setPlaceholderText("0.0")
        grid_layout.addWidget(self.inputs['interval'], 3, 1)

        layout.addLayout(grid_layout)

        # Кнопка добавления
        add_btn = QPushButton("Добавить данные")
        add_btn.clicked.connect(self.add_data)
        add_btn.setStyleSheet("background: #4CAF50; color: white; padding: 10px;")
        layout.addWidget(add_btn)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        headers = [
            "Год", "Отказы 1", "Отказы 2", "Отказы 3", "Поездопотери",
            "Кап. вложения", "Пассажиры", "Тех. отказы", "Стоимость", "Интервал", "Действия"
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.setWindowTitle("Ввод данных МЦК")
        self.resize(1500, 650)

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

            delete_btn = QPushButton("Удалить")
            delete_btn.setStyleSheet("background: #f44336; color: white;")
            delete_btn.clicked.connect(lambda checked, y=record.year: self.delete_record(y))
            self.table.setCellWidget(row, 10, delete_btn)

    def delete_record(self, year):
        try:
            db = next(get_db())
            delete_data(db, year)
            self.load_data()
            QMessageBox.information(self, "Успех", f"Данные за {year} год удалены!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка удаления: {str(e)}")
