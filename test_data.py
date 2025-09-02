from libs.database import SessionLocal, init_db
from controllers.data_crud import create_mck_data


def add_test_data():
    init_db()
    db = SessionLocal()

    # Полные данные за 2016–2024 годы
    test_data = [
        # year, f1, f2, f3, train_losses, investments, passengers_daily, tech_failures, fare_cost, interval
        (2016, 0, 20, 6, 87.91, 32561.74, 239186, 2, 50.0, 8.0),
        (2017, 0, 10, 37, 314.17, 38310.05, 302919, 1, 55.0, 8.0),
        (2018, 1, 3, 18, 53.13, 45684.21, 354665, 1, 55.0, 8.0),
        (2019, 1, 2, 10, 59.13, 74860.95, 405773, 0, 55.0, 5.9151),
        (2020, 0, 5, 6, 186.01, 101163.12, 315804, 0, 57.0, 5.9151),
        (2021, 1, 0, 7, 188.03, 114465.14, 409985, 0, 60.0, 5.9151),
        (2022, 0, 4, 5, 83.40, 123292.90, 433924, 0, 61.0, 5.9151),
        (2023, 0, 6, 7, 8.45, 189559.28, 427944, 0, 62.0, 5.9151),
        (2024, 0, 1, 3, 0.20, 40742.78, 452441, 0, 70.0, 5.9151),
    ]

    for record in test_data:
        create_mck_data(db, *record)

    db.close()
    print("✅ Тестовые данные за 2016–2024 годы добавлены!")


if __name__ == "__main__":
    add_test_data()
