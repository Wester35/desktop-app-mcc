from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox, \
    QFrame
from controllers.crud import update_user_password, get_user_data, get_user_full_name


class ProfileWindow(QWidget):
    def __init__(self, user_id, is_admin):
        super().__init__()
        self.user_id = user_id
        self.is_admin = is_admin
        self.setWindowTitle("Профиль пользователя")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()
        self.load_user_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        title_style = "font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 5px;"
        label_style = "font-size: 14px; color: #34495e; padding: 5px;"
        line_edit_style = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
                background-color: transparent;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: transparent;
            }
        """
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """


        profile_header = QLabel("Профиль пользователя")
        profile_header.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(profile_header)


        info_group = QGroupBox("Личная информация")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ecf0f1;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #7f8c8d;
            }
        """)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)

        self.name_label = QLabel("Полное имя: ")
        self.login_label = QLabel("Логин: ")
        self.phone_label = QLabel("Телефон: ")
        self.role_label = QLabel("Роль: ")

        for label in [self.name_label, self.login_label, self.phone_label, self.role_label]:
            label.setStyleSheet(label_style)
            info_layout.addWidget(label)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)


        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #ecf0f1; margin: 15px 0;")
        layout.addWidget(separator)


        password_group = QGroupBox("Изменение пароля")
        password_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ecf0f1;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #7f8c8d;
            }
        """)

        password_layout = QVBoxLayout()
        password_layout.setSpacing(12)


        current_pass_label = QLabel("Текущий пароль:")
        current_pass_label.setStyleSheet("font-weight: bold; color: #34495e;")

        self.current_password_edit = QLineEdit()
        self.current_password_edit.setPlaceholderText("Введите текущий пароль")
        self.current_password_edit.setEchoMode(QLineEdit.Password)
        self.current_password_edit.setStyleSheet(line_edit_style)


        new_pass_label = QLabel("Новый пароль:")
        new_pass_label.setStyleSheet("font-weight: bold; color: #34495e;")

        self.new_password_edit = QLineEdit()
        self.new_password_edit.setPlaceholderText("Введите новый пароль")
        self.new_password_edit.setEchoMode(QLineEdit.Password)
        self.new_password_edit.setStyleSheet(line_edit_style)


        confirm_pass_label = QLabel("Подтверждение пароля:")
        confirm_pass_label.setStyleSheet("font-weight: bold; color: #34495e;")

        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("Повторите новый пароль")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setStyleSheet(line_edit_style)


        password_layout.addWidget(current_pass_label)
        password_layout.addWidget(self.current_password_edit)
        password_layout.addWidget(new_pass_label)
        password_layout.addWidget(self.new_password_edit)
        password_layout.addWidget(confirm_pass_label)
        password_layout.addWidget(self.confirm_password_edit)


        self.change_password_btn = QPushButton("Изменить пароль")
        self.change_password_btn.clicked.connect(self.change_password)
        self.change_password_btn.setStyleSheet(button_style)
        self.change_password_btn.setCursor(Qt.PointingHandCursor)

        password_layout.addWidget(self.change_password_btn)
        password_group.setLayout(password_layout)
        layout.addWidget(password_group)

        layout.addStretch()

        self.setLayout(layout)

    def load_user_data(self):
        user_data = get_user_data(self.user_id)
        print(f"Данные пользователя: {user_data}")  # Для отладки

        if user_data:
            # Формируем полное имя из компонентов
            name_parts = []
            if user_data['last_name']:
                name_parts.append(user_data['last_name'])
            if user_data['first_name']:
                name_parts.append(user_data['first_name'])
            if user_data['middle_name']:
                name_parts.append(user_data['middle_name'])

            full_name = ' '.join(name_parts) if name_parts else user_data['login']

            self.name_label.setText(f"Полное имя: {full_name}")
            self.login_label.setText(f"Логин: {user_data['login']}")
            self.phone_label.setText(f"Телефон: {user_data['phone'] or 'Не указан'}")
            role = "Администратор" if self.is_admin else "Пользователь"
            self.role_label.setText(f"Роль: {role}")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные пользователя")
            self.name_label.setText("Полное имя: Ошибка загрузки")
            self.login_label.setText("Логин: Ошибка загрузки")
            self.phone_label.setText("Телефон: Ошибка загрузки")
            self.role_label.setText(f"Роль: {'Администратор' if self.is_admin else 'Пользователь'}")

    def change_password(self):
        current_password = self.current_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if not current_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Новые пароли не совпадают")
            return

        if len(new_password) < 6:
            QMessageBox.warning(self, "Ошибка", "Пароль должен содержать минимум 6 символов")
            return

        success = update_user_password(self.user_id, current_password, new_password)

        if success:
            QMessageBox.information(self, "Успех", "Пароль успешно изменен")
            self.clear_password_fields()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный текущий пароль или ошибка при изменении")

    def clear_password_fields(self):
        self.current_password_edit.clear()
        self.new_password_edit.clear()
        self.confirm_password_edit.clear()