from sqlalchemy import Column, Integer, Float, DateTime
from libs.database import Base
from datetime import datetime

class MCKData(Base):
    __tablename__ = "mck_data"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True, index=True)  # Год
    failures_1 = Column(Integer)  # Отказы 1 категории
    failures_2 = Column(Integer)  # Отказы 2 категории
    failures_3 = Column(Integer)  # Отказы 3 категории
    train_losses = Column(Float)  # Поездопотери, поезд/час
    investments = Column(Float)  # Капитальные вложения, млн руб.
    passengers_daily = Column(Integer)  # Среднесуточное количество пассажиров, чел.
    tech_failures = Column(Integer)  # Отказы технических средств, раз
    fare_cost = Column(Float)  # Стоимость оплаты проезда, руб.
    interval = Column(Float)

    def __repr__(self):
        return f"<MCKData {self.year}>"

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    integrated_index = Column(Float)  # y_оконч
    created_at = Column(DateTime, default=datetime.now)