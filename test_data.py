import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import seaborn as sns
import statsmodels.api as sm
# Данные из таблицы 1
data = {
    'Year': [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Failure_1': [0, 0, 1, 1, 0, 1, 0, 0, 0],
    'Failure_2': [20, 10, 3, 2, 5, 0, 4, 6, 1],
    'Failure_3': [6, 37, 18, 10, 6, 7, 5, 7, 3],
    'Train_Losses': [87.91, 314.17, 53.13, 59.13, 186.01, 188.03, 83.4, 8.45, 0.2],
    'Capital_Investment': [32561.738, 38310.052, 45684.214, 74860.946, 101163.119, 114465.137, 123292.895, 189559.28, 40742.776],
    'Passengers_Daily': [239186, 302919, 354665, 405773, 315804, 409985, 433924, 427944, 452441],
    'Tech_Failures': [2, 1, 1, 0, 0, 0, 0, 0, 0],
    'Ticket_Price': [50, 55, 55, 55, 57, 60, 61, 62, 70],
    'Interval': [8, 8, 8, 5.9151, 5.9151, 5.9151, 5.9151, 5.9151, 5.9151],
    'Aggregated_Indicator': [1.0829, 1.1614, 0.5931, 0.4785, 1.2012, 0.6829, 1.3483, 1.4122, 1.4287]
}

df = pd.DataFrame(data)

# Уравнение 6: Качество обслуживания = f(Интервал, Отказы 1 категории)
print("=== УРАВНЕНИЕ 6: Качество обслуживания ===")
print("y = 1.7359 - 0.0701 * Interval - 0.6876 * Failure_1")

# Подготовка данных для уравнения 6
X6 = df[['Interval', 'Failure_1']]
y6 = df['Aggregated_Indicator']

# Добавляем константу для регрессии
X6_with_const = sm.add_constant(X6)

# Строим регрессионную модель
model6 = sm.OLS(y6, X6_with_const).fit()

print("\nРезультаты регрессии (уравнение 6):")
print(model6.summary())

# Прогноз и доверительные интервалы для уравнения 6
predictions6 = model6.get_prediction(X6_with_const)
pred_summary6 = predictions6.summary_frame(alpha=0.05)

df['Predicted_Quality'] = pred_summary6['mean']
df['CI_lower_6'] = pred_summary6['mean_ci_lower']
df['CI_upper_6'] = pred_summary6['mean_ci_upper']

# Уравнение 7: Интервал движения = f(Отказы 3 категории, Технические отказы)
print("\n=== УРАВНЕНИЕ 7: Интервал движения ===")
print("y = 5.7169 + 0.0359 * Failure_3 + 1.1213 * Tech_Failures")

# Подготовка данных для уравнения 7
X7 = df[['Failure_3', 'Tech_Failures']]
y7 = df['Interval']

# Добавляем константу для регрессии
X7_with_const = sm.add_constant(X7)

# Строим регрессионную модель
model7 = sm.OLS(y7, X7_with_const).fit()

print("\nРезультаты регрессии (уравнение 7):")
print(model7.summary())

# Прогноз и доверительные интервалы для уравнения 7
predictions7 = model7.get_prediction(X7_with_const)
pred_summary7 = predictions7.summary_frame(alpha=0.05)

df['Predicted_Interval'] = pred_summary7['mean']
df['CI_lower_7'] = pred_summary7['mean_ci_lower']
df['CI_upper_7'] = pred_summary7['mean_ci_upper']

# Визуализация результатов
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# График 1: Уравнение 6 - Фактические vs Предсказанные значения
axes[0, 0].plot(df['Year'], df['Aggregated_Indicator'], 'bo-', label='Фактические значения', linewidth=2, markersize=8)
axes[0, 0].plot(df['Year'], df['Predicted_Quality'], 'ro--', label='Предсказанные значения', linewidth=2, markersize=6)
axes[0, 0].fill_between(df['Year'], df['CI_lower_6'], df['CI_upper_6'], alpha=0.3, color='red', label='95% Доверительный интервал')
axes[0, 0].set_title('Уравнение 6: Качество обслуживания\n(Агрегированный показатель)', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Год')
axes[0, 0].set_ylabel('Агрегированный показатель качества')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# График 2: Уравнение 6 - Остатки
residuals6 = df['Aggregated_Indicator'] - df['Predicted_Quality']
axes[0, 1].scatter(df['Predicted_Quality'], residuals6, alpha=0.7, s=80)
axes[0, 1].axhline(y=0, color='red', linestyle='--', alpha=0.8)
axes[0, 1].set_title('Уравнение 6: График остатков', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Предсказанные значения')
axes[0, 1].set_ylabel('Остатки')
axes[0, 1].grid(True, alpha=0.3)

# График 3: Уравнение 7 - Фактические vs Предсказанные значения
axes[1, 0].plot(df['Year'], df['Interval'], 'bo-', label='Фактические значения', linewidth=2, markersize=8)
axes[1, 0].plot(df['Year'], df['Predicted_Interval'], 'ro--', label='Предсказанные значения', linewidth=2, markersize=6)
axes[1, 0].fill_between(df['Year'], df['CI_lower_7'], df['CI_upper_7'], alpha=0.3, color='red', label='95% Доверительный интервал')
axes[1, 0].set_title('Уравнение 7: Интервал движения поездов', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Год')
axes[1, 0].set_ylabel('Интервал движения (минуты)')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# График 4: Уравнение 7 - Остатки
residuals7 = df['Interval'] - df['Predicted_Interval']
axes[1, 1].scatter(df['Predicted_Interval'], residuals7, alpha=0.7, s=80)
axes[1, 1].axhline(y=0, color='red', linestyle='--', alpha=0.8)
axes[1, 1].set_title('Уравнение 7: График остатков', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Предсказанные значения')
axes[1, 1].set_ylabel('Остатки')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Дополнительная информация
print("\n=== СТАТИСТИЧЕСКИЕ ХАРАКТЕРИСТИКИ ===")
print(f"Уравнение 6 - R²: {model6.rsquared:.4f}")
print(f"Уравнение 6 - Скорректированный R²: {model6.rsquared_adj:.4f}")
print(f"Уравнение 7 - R²: {model7.rsquared:.4f}")
print(f"Уравнение 7 - Скорректированный R²: {model7.rsquared_adj:.4f}")

# Проверка значимости коэффициентов
print("\n=== ПРОВЕРКА ЗНАЧИМОСТИ КОЭФФИЦИЕНТОВ (t-тест) ===")
print("Уравнение 6:")
for i, coef in enumerate(model6.params):
    p_value = model6.pvalues[i]
    significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "незначим"
    print(f"  Коэффициент {i}: {coef:.4f} (p-value: {p_value:.4f}) - {significance}")

print("Уравнение 7:")
for i, coef in enumerate(model7.params):
    p_value = model7.pvalues[i]
    significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "незначим"
    print(f"  Коэффициент {i}: {coef:.4f} (p-value: {p_value:.4f}) - {significance}")