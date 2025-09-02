from libs.database import SessionLocal, init_db
from controllers.data_crud import create_mck_data


def add_test_data():
    init_db()
    db = SessionLocal()

    # Пример данных за 2020-2024 годы согласно новым полям
    test_data = [
        # year, f1, f2, f3, train_loss, invest, pass_daily, tech_fail, fare
        (2020, 2, 5, 8, 1.2, 1200.5, 150000, 3, 45.0),
        (2021, 1, 4, 6, 0.8, 1500.3, 160000, 2, 46.5),
        (2022, 0, 3, 5, 0.5, 1800.7, 170000, 1, 48.0),
        (2023, 1, 2, 4, 0.3, 2000.2, 180000, 0, 50.0),
        (2024, 0, 1, 3, 0.1, 2200.9, 190000, 0, 52.5)
    ]

    for data in test_data:
        create_mck_data(db, *data)

    db.close()
    print("Тестовые данные добавлены!")


if __name__ == "__main__":
    add_test_data()