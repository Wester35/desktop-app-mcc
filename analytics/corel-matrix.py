import pandas as pd
import numpy as np


data = {
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
    'interval': [8, 8, 8, 5.9151, 5.9151, 5.9151, 5.9151, 5.9151, 5.9151],
    'integral': [1.0829, 1.1614, 0.5931, 0.4785, 1.2012, 0.6829, 1.3483, 1.4122, 1.4287]
}

df = pd.DataFrame(data)
pd.set_option('display.max_rows', None)  # Показать все строки
pd.set_option('display.max_columns', None)  # Показать все столбцы
pd.set_option('display.width', None)  # Без ограничения ширины
pd.set_option('display.max_colwidth', None)  # Без ограничения ширины столбцов
pd.set_option('display.float_format', '{:.4f}'.format)
# 1. Автоматический расчет (рекомендуется)
correlation_matrix = df.corr()
print("Матрица корреляции:")
print(correlation_matrix.round(15))