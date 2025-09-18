from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
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

        # Личная информация
        self.name_label = QLabel("Полное имя: ")
        self.login_label = QLabel("Логин: ")
        self.phone_label = QLabel("Телефон: ")
        self.role_label = QLabel("Роль: ")

        # Разделитель
        layout.addWidget(QLabel("─" * 50))

        # Поля для изменения пароля
        self.current_password_edit = QLineEdit()
        self.current_password_edit.setPlaceholderText("Текущий пароль")
        self.current_password_edit.setEchoMode(QLineEdit.Password)

        self.new_password_edit = QLineEdit()
        self.new_password_edit.setPlaceholderText("Новый пароль")
        self.new_password_edit.setEchoMode(QLineEdit.Password)

        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("Подтвердите новый пароль")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)

        # Кнопка изменения пароля
        self.change_password_btn = QPushButton("Изменить пароль")
        self.change_password_btn.clicked.connect(self.change_password)

        # Добавляем элементы в layout
        layout.addWidget(QLabel("<b>Личная информация:</b>"))
        layout.addWidget(self.name_label)
        layout.addWidget(self.login_label)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.role_label)

        layout.addWidget(QLabel("\n<b>Изменение пароля:</b>"))
        layout.addWidget(self.current_password_edit)
        layout.addWidget(self.new_password_edit)
        layout.addWidget(self.confirm_password_edit)
        layout.addWidget(self.change_password_btn)

        self.setLayout(layout)

    def load_user_data(self):
        """Загрузка данных пользователя"""
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
        """Изменение пароля пользователя"""
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

        # Вызов функции для изменения пароля
        success = update_user_password(self.user_id, current_password, new_password)

        if success:
            QMessageBox.information(self, "Успех", "Пароль успешно изменен")
            self.clear_password_fields()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный текущий пароль или ошибка при изменении")

    def clear_password_fields(self):
        """Очистка полей пароля"""
        self.current_password_edit.clear()
        self.new_password_edit.clear()
        self.confirm_password_edit.clear()