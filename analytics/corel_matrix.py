from typing import List
import pandas as pd
from sqlalchemy.orm import Session
from models.data_models import MCKData, AnalysisResult


def get_data_1(db: Session, years: List[int]):
    data_records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()
    integral_records = (
        db.query(AnalysisResult).filter(AnalysisResult.year.in_(years)).order_by(AnalysisResult.year).all())

    integral_dict = {rec.year: rec.integrated_index for rec in integral_records}

    raw_data = []
    for rec in data_records:
        raw_data.append({
            'failures_1': rec.failures_1,
            'failures_2': rec.failures_2,
            'failures_3': rec.failures_3,
            'train_losses': rec.train_losses,
            'investments': rec.investments,
            'passengers_daily': rec.passengers_daily,
            'tech_failures': rec.tech_failures,
            'fare_cost': rec.fare_cost,
            'interval': rec.interval,
            'integrated_index': integral_dict.get(rec.year)
        })

    return raw_data


def get_data_2(db: Session, years: List[int]):
    data_records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()

    raw_data = []
    for rec in data_records:
        raw_data.append({
            'failures_1': rec.failures_1,
            'failures_2': rec.failures_2,
            'failures_3': rec.failures_3,
            'train_losses': rec.train_losses,
            'investments': rec.investments,
            'passengers_daily': rec.passengers_daily,
            'tech_failures': rec.tech_failures,
            'fare_cost': rec.fare_cost,
            'interval': rec.interval,
        })

    return raw_data

def get_correl_matrix(db: Session, years: List[int]):
    data = get_data_1(db, years)
    df = pd.DataFrame(data)
    correlation_matrix = df.corr().round(15)
    return correlation_matrix

def get_second_correl_matrix(db: Session, years: List[int]):
    data = get_data_2(db, years)
    df = pd.DataFrame(data)
    correlation_matrix = df.corr().round(15)
    return correlation_matrix


