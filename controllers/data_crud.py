from sqlalchemy.orm import Session
from models.data_models import MCKData
import pandas as pd


def create_mck_data(db: Session, year: int, failures_1: int, failures_2: int,
                   failures_3: int, train_losses: float, investments: float,
                   passengers_daily: int, tech_failures: int, fare_cost: float, interval: float):
    """Создание новой записи данных МЦК"""
    try:
        data = MCKData(
            year=year,
            failures_1=failures_1,
            failures_2=failures_2,
            failures_3=failures_3,
            train_losses=train_losses,
            investments=investments,
            passengers_daily=passengers_daily,
            tech_failures=tech_failures,
            fare_cost=fare_cost,
            interval=interval
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        db.rollback()
        raise e

def get_all_data(db: Session):
    """Получение всех данных"""
    return db.query(MCKData).order_by(MCKData.year).all()

def get_data_by_year(db: Session, year: int):
    """Получение данных по году"""
    return db.query(MCKData).filter(MCKData.year == year).first()

def delete_data(db: Session, year: int):
    """Удаление данных по году"""
    data = db.query(MCKData).filter(MCKData.year == year).first()
    if data:
        db.delete(data)
        db.commit()
    return data

def update_data(db: Session, year: int, **kwargs):
    """Обновление данных"""
    data = db.query(MCKData).filter(MCKData.year == year).first()
    if data:
        for key, value in kwargs.items():
            setattr(data, key, value)
        db.commit()
        db.refresh(data)
    return data


def get_all_data_dataframe(db: Session) -> pd.DataFrame:
    """Получение всех данных в виде DataFrame"""
    try:
        # Вариант 1: Через SQLAlchemy query (проще)
        data = db.query(MCKData).order_by(MCKData.year).all()
        # Преобразуем в список словарей
        data_dicts = []
        for record in data:
            data_dicts.append({
                'year': record.year,
                'failures_1': record.failures_1,
                'failures_2': record.failures_2,
                'failures_3': record.failures_3,
                'train_losses': record.train_losses,
                'investments': record.investments,
                'passengers_daily': record.passengers_daily,
                'tech_failures': record.tech_failures,
                'fare_cost': record.fare_cost,
                'interval': record.interval,
                'profitability': record.profitability,
                'cap_invest_interval': record.cap_invest_interval
            })

        return pd.DataFrame(data_dicts)

    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return pd.DataFrame()