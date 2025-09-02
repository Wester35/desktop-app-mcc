from sqlalchemy.orm import Session
from models.data_models import MCKData

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