from decimal import Decimal, getcontext
import pandas as pd



from typing import List, Dict
import numpy as np

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

def get_data(years: List[int]) -> pd.DataFrame:
    data = {
        'year': [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        'failures_1': [0, 0, 1, 1, 0, 1, 0, 0, 0],                      #2
        'failures_2': [20, 10, 3, 2, 5, 0, 4, 6, 1],                    #2
        'failures_3': [6, 37, 18, 10, 6, 7, 5, 7, 3],                   #2
        'train_losses': [87.91, 314.17, 53.13, 59.13, 186.01, 188.03, 83.4, 8.45, 0.2],#2
        'investments': [32561.738, 38310.052, 45684.214, 74860.946, 101163.119,        #1
                        114465.137, 123292.895, 189559.28, 40742.776],
        'passengers_daily': [239186, 302919, 354665, 405773, 315804,    #2
                             409985, 433924, 427944, 452441],
        'tech_failures': [2, 1, 1, 0, 0, 0, 0, 0, 0],                   #1
        'fare_cost': [50, 55, 55, 55, 57, 60, 61, 62, 70],              #1
        'interval': [8, 8, 8, 5.9151, 5.9151, 5.9151, 5.9151, 5.9151, 5.9151] #1
    }
    return pd.DataFrame(data)


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

    # Создаем новый DataFrame для нормализованных данных
    normalize_df = pd.DataFrame()

    # Нормализуем каждый столбец
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


def calculate(normalized: pd.DataFrame) -> pd.DataFrame:
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

    return y5_stage

pd.set_option('display.max_rows', None)  # Показать все строки
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', None)  # Без ограничения ширины
pd.set_option('display.max_colwidth', None)  # Без ограничения ширины столбцов
pd.set_option('display.float_format', '{:.15f}'.format)

years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
print(get_data(years))
print("\n"+"="*80 + "\n")
df = get_data(years)
print(normalize_data(df))
print("\n"+"="*80 + "\n")
print(calculate(normalize_data(df)))

