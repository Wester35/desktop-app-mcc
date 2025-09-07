import pandas as pd
import numpy as np
import statsmodels.api as sm
from analytics.corel_matrix import get_correl_matrix
from controllers.data_crud import get_all_data
from libs.database import get_db
from models.data_models import AnalysisResult  # Импортируем модель


def get_integral_indicators(correl_matrix: pd.DataFrame, stock_data: pd.DataFrame):
    integral_correl = correl_matrix['integrated_index'].round(15)
    y_columns = integral_correl[(abs(integral_correl) > 0.19) & (integral_correl.index != 'integrated_index')]
    x_columns_labels = y_columns.index.tolist()
    available_columns = [col for col in x_columns_labels if col in stock_data.columns]

    return y_columns, stock_data[available_columns]


def get_y_data_from_db(db, years):
    """Получаем реальные значения integrated_index из базы данных"""
    # Запрос к базе данных для получения y_окончательного
    results = db.query(AnalysisResult).filter(AnalysisResult.year.in_(years)).order_by(AnalysisResult.year).all()

    # Создаем Series с годами в качестве индекса
    y_data = pd.Series(
        {result.year: result.integrated_index for result in results},
        name='integrated_index'
    )

    return y_data


def excel_style_regression(y_data, x_data, add_constant=True, confidence_level=0.95):
    """Регрессионный анализ в стиле Excel"""
    # Убедимся, что индексы совпадают
    common_index = y_data.index.intersection(x_data.index)
    y_data = y_data.loc[common_index]
    x_data = x_data.loc[common_index]

    # Добавляем константу
    if add_constant:
        X = sm.add_constant(x_data)
    else:
        X = x_data

    # Создаем и обучаем модель
    model = sm.OLS(y_data, X)
    results = model.fit()

    # Регрессионная статистика
    n_obs = len(y_data)
    k_vars = len(results.params) - 1 if add_constant else len(results.params)

    regression_stats = pd.DataFrame({
        'Показатель': ['Множественный R', 'R-квадрат', 'Нормированный R-квадрат',
                       'Стандартная ошибка', 'Наблюдения'],
        'Значение': [np.sqrt(results.rsquared), results.rsquared, results.rsquared_adj,
                     np.sqrt(results.mse_resid), n_obs]
    })

    # Дисперсионный анализ
    anova_data = {
        '': ['Регрессия', 'Остаток', 'Итого'],
        'df': [k_vars, n_obs - k_vars - 1, n_obs - 1],
        'SS': [results.ess, results.ssr, results.ess + results.ssr],
        'MS': [results.ess / k_vars, results.mse_resid, np.nan],
        'F': [results.fvalue, np.nan, np.nan],
        'Значимость F': [results.f_pvalue, np.nan, np.nan]
    }
    anova_df = pd.DataFrame(anova_data)

    # Коэффициенты
    alpha = 1 - confidence_level
    conf_int = results.conf_int(alpha=alpha)

    variable_names = ['Y-пересечение']
    variable_names.extend([f'Переменная X {i + 1} ({col})' for i, col in enumerate(x_data.columns)])

    coefficients_df = pd.DataFrame({
        '': variable_names,
        'Коэффициенты': results.params,
        'Стандартная ошибка': results.bse,
        't-статистика': results.tvalues,
        'P-Значение': results.pvalues,
        'Нижние 95%': conf_int[0],
        'Верхние 95%': conf_int[1]
    })

    return regression_stats, anova_df, coefficients_df, results


def calc_regression():
    db = next(get_db())

    # Получаем данные
    data_records = get_all_data(db)
    years = [record.year for record in data_records]

    from analytics.ryab import get_data as get_mcc_data
    stock_data = get_mcc_data(db, years)
    correl_matrix = get_correl_matrix(db, years)

    # Получаем коэффициенты и данные для регрессии (X variables)
    coefficients, x_data = get_integral_indicators(correl_matrix=correl_matrix, stock_data=stock_data)

    # Получаем реальные значения Y из базы данных
    y_data = get_y_data_from_db(db, years)

    print("ДАННЫЕ ДЛЯ РЕГРЕССИИ:")
    print(f"Годы анализа: {years}")
    print(f"\nY переменная (integrated_index из базы):")
    print(y_data)
    print(f"\nX переменные (признаки):")
    print(x_data)
    print(f"\nКоэффициенты корреляции:")
    print(coefficients)
    print("\n" + "=" * 60)

    # Проверяем совпадение индексов
    common_years = sorted(list(set(y_data.index).intersection(set(x_data.index))))
    print(f"Общие годы для анализа: {common_years}")
    print(f"Количество наблюдений: {len(common_years)}")

    # Фильтруем данные по общим годам
    y_data = y_data.loc[common_years]
    x_data = x_data.loc[common_years]

    # Выполняем регрессионный анализ
    regression_stats, anova_df, coefficients_df, results = excel_style_regression(
        y_data, x_data, add_constant=True, confidence_level=0.95
    )

    # Выводим результаты в стиле Excel
    print("\nВЫВОД ИТОГОВ")
    print(" " * 32 + "Регрессионная статистика")
    print(regression_stats.to_string(index=False, header=False))
    print("\n" + " " * 16 + "Дисперсионный анализ")
    print(anova_df.to_string(index=False))
    print("\n" + " " * 8 + "Коэффициенты и статистики")
    print(coefficients_df.to_string(index=False))

    # Дополнительная информация
    print("\n" + "=" * 60)
    print("ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")

    # Уравнение регрессии
    equation = f"integrated_index = {results.params['const']:.6f}"
    for feature in x_data.columns:
        coef = results.params[feature]
        sign = " + " if coef >= 0 else " - "
        equation += f"{sign}{abs(coef):.6f}*{feature}"
    print(f"Уравнение регрессии:\n{equation}")

    print(f"\nR-квадрат: {results.rsquared:.6f}")
    print(f"Скорректированный R-квадрат: {results.rsquared_adj:.6f}")
    print(f"F-статистика: {results.fvalue:.6f} (p-value: {results.f_pvalue:.6f})")


    return results


if __name__ == "__main__":
    # Настройки отображения
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.float_format', '{:.6f}'.format)

    try:
        results = calc_regression()
        print("\nАнализ завершен успешно!")
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback

        traceback.print_exc()