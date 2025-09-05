from decimal import Decimal, getcontext
import pandas as pd
from typing import List, Dict
import numpy as np
from sqlalchemy.orm import Session
from models.data_models import MCKData


getcontext().prec = 15
columns_in_norm = ['failures_1', 'failures_2', 'failures_3',
                   'train_losses', 'investments', 'passengers_daily',
                   'tech_failures', 'fare_cost', 'interval']


def excel_normalize(value, min_val, max_val, reverse=False):
    """Нормализация как в Excel"""
    if max_val == min_val:
        return Decimal('0.5')

    value_dec = Decimal(str(value))
    min_dec = Decimal(str(min_val))
    max_dec = Decimal(str(max_val))

    if reverse:
        result = (max_dec - value_dec) / (max_dec - min_dec)
    else:
        result = (value_dec - min_dec) / (max_dec - min_dec)

    return float(result)

def get_data(db: Session, years: List[int]) -> pd.DataFrame:
    data_records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()

    # Создаем DataFrame с исходными данными
    raw_data = []
    for rec in data_records:
        raw_data.append({
            'year': rec.year,
            'failures_1': rec.failures_1,
            'failures_2': rec.failures_2,
            'failures_3': rec.failures_3,
            'train_losses': rec.train_losses,
            'investments': rec.investments,
            'passengers_daily': rec.passengers_daily,
            'tech_failures': rec.tech_failures,
            'fare_cost': rec.fare_cost,
            'interval': rec.interval
        })

    df_raw = pd.DataFrame(raw_data).set_index('year')

    return pd.DataFrame(df_raw)


def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    min_max_dict = {}

    # Проходим по всем числовым столбцам (исключая год)
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    if 'year' in numeric_columns:
        numeric_columns = numeric_columns.drop('year')

    for column in numeric_columns:
        min_val = data[column].min()
        max_val = data[column].max()
        min_max_dict[column] = {'min': min_val, 'max': max_val}

    normalize_df = pd.DataFrame()

    normalize_df['failures_1'] = data['failures_1'].apply(
        lambda x: excel_normalize(x, min_max_dict['failures_1']['min'],
                                  min_max_dict['failures_1']['max'], reverse=True)
    )

    normalize_df['failures_2'] = data['failures_2'].apply(
        lambda x: excel_normalize(x, min_max_dict['failures_2']['min'],
                                  min_max_dict['failures_2']['max'], reverse=True)
    )

    normalize_df['failures_3'] = data['failures_3'].apply(
        lambda x: excel_normalize(x, min_max_dict['failures_3']['min'],
                                  min_max_dict['failures_3']['max'], reverse=True)
    )

    normalize_df['train_losses'] = data['train_losses'].apply(
        lambda x: excel_normalize(x, min_max_dict['train_losses']['min'],
                                  min_max_dict['train_losses']['max'])
    )

    normalize_df['investments'] = data['investments'].apply(
        lambda x: excel_normalize(x, min_max_dict['investments']['min'],
                                  min_max_dict['investments']['max'])
    )

    normalize_df['passengers_daily'] = data['passengers_daily'].apply(
        lambda x: excel_normalize(x, min_max_dict['passengers_daily']['min'],
                                  min_max_dict['passengers_daily']['max'])
    )

    normalize_df['tech_failures'] = data['tech_failures'].apply(
        lambda x: excel_normalize(x, min_max_dict['tech_failures']['min'],
                                  min_max_dict['tech_failures']['max'])
    )

    normalize_df['fare_cost'] = data['fare_cost'].apply(
        lambda x: excel_normalize(x, min_max_dict['fare_cost']['min'],
                                  min_max_dict['fare_cost']['max'])
    )

    normalize_df['interval'] = data['interval'].apply(
        lambda x: excel_normalize(x, min_max_dict['interval']['min'],
                                  min_max_dict['interval']['max'])
    )
    normalize_df = normalize_df.round(15)
    return normalize_df


def calculate(normalized: pd.DataFrame):
    #1
    row_means = normalized.mean(axis=1)
    
    correlation_results = pd.DataFrame(index=normalized.columns, columns=['correlation'])

    for column in normalized.columns:
        corr_value = normalized[column].corr(row_means)
        correlation_results.loc[column, 'correlation'] = corr_value

    correlation_results = correlation_results.astype(float)
    sum_correlation = correlation_results.values.sum()
    weights = abs(correlation_results / sum_correlation).round(15)

    #2
    y2_stage = pd.DataFrame()

    weighted_sum = pd.Series(0, index=normalized.index)

    for column in normalized.columns:
        column_weight = weights.loc[column, 'correlation']
        weighted_sum += normalized[column] * column_weight

    y2_stage['weighted_sum'] = weighted_sum

    correlation_results = pd.DataFrame(index=normalized.columns, columns=['correlation'])

    for column in normalized.columns:
        corr_value = normalized[column].corr(weighted_sum)
        correlation_results.loc[column, 'correlation'] = corr_value

    sum_correlation = correlation_results.values.sum()
    weights = abs(correlation_results / sum_correlation).round(15)

    #3
    y3_stage = pd.DataFrame()

    weighted_sum = pd.Series(0, index=normalized.index)

    for column in normalized.columns:
        column_weight = weights.loc[column, 'correlation']
        weighted_sum += normalized[column] * column_weight

    y3_stage['weighted_sum'] = weighted_sum

    correlation_results = pd.DataFrame(index=normalized.columns, columns=['correlation'])

    for column in normalized.columns:
        corr_value = normalized[column].corr(weighted_sum)
        correlation_results.loc[column, 'correlation'] = corr_value

    sum_correlation = correlation_results.values.sum()
    weights = abs(correlation_results / sum_correlation).round(15)

    #4
    y4_stage = pd.DataFrame()
    weighted_sum = pd.Series(0, index=normalized.index)

    for column in normalized.columns:
        column_weight = weights.loc[column, 'correlation']
        weighted_sum += normalized[column] * column_weight

    y4_stage['weighted_sum'] = weighted_sum

    correlation_results = pd.DataFrame(index=normalized.columns, columns=['correlation'])

    for column in normalized.columns:
        corr_value = normalized[column].corr(weighted_sum)
        correlation_results.loc[column, 'correlation'] = corr_value

    sum_correlation = correlation_results.values.sum()
    weights = abs(correlation_results / sum_correlation).round(15)

    #5
    y5_stage = pd.DataFrame()
    weighted_sum = pd.Series(0, index=normalized.index)

    for column in normalized.columns:
        column_weight = weights.loc[column, 'correlation']
        weighted_sum += normalized[column] * column_weight

    y5_stage['weighted_sum'] = weighted_sum

    correlation_results = pd.DataFrame(index=normalized.columns, columns=['correlation'])

    for column in normalized.columns:
        corr_value = normalized[column].corr(weighted_sum)
        correlation_results.loc[column, 'correlation'] = corr_value

    sum_correlation = correlation_results.values.sum()
    weights = abs(correlation_results / sum_correlation).round(15)

    return y5_stage, weights

pd.set_option('display.max_rows', None)  # Показать все строки
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', None)  # Без ограничения ширины
pd.set_option('display.max_colwidth', None)  # Без ограничения ширины столбцов
pd.set_option('display.float_format', '{:.15f}'.format)
