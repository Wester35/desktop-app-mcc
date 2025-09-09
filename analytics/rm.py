import pandas as pd
import numpy as np
import statsmodels.api as sm
from analytics.corel_matrix import get_correl_matrix, get_second_correl_matrix
from controllers.data_crud import get_all_data
from libs.database import get_db
from models.data_models import AnalysisResult, MCKData
from analytics.constants import t_criteria_list, F_CRITICAL_VALUES


def get_f_critical(k1, k2):
    """
    Получить критическое значение F-критерия Фишера для α=0.05

    Args:
        k1: степени свободы числителя (количество факторов)
        k2: степени свободы знаменателя (n - k1 - 1)

    Returns:
        Критическое значение F-критерия
    """
    # Если точное значение есть в таблице - возвращаем его
    if k1 in F_CRITICAL_VALUES and k2 in F_CRITICAL_VALUES[k1]:
        return F_CRITICAL_VALUES[k1][k2]

    # Аппроксимация для больших значений
    # Для k2 > 10 используем приближение из последней строки таблицы (∞)
    if k2 > 10:
        if k1 == 1: return 254.32
        if k1 == 2: return 19.50
        if k1 == 3: return 8.53
        if k1 == 4: return 5.63
        if k1 == 5: return 4.36
        if k1 == 6: return 3.67
        if k1 == 7: return 3.23
        if k1 == 8: return 2.93
        if k1 == 9: return 2.71
        if k1 == 10: return 2.54

    # Консервативное значение по умолчанию
    return 4.0

def get_integral_indicators(correl_matrix: pd.DataFrame, stock_data: pd.DataFrame):
    integral_correl = correl_matrix['integrated_index'].round(15)

    # Отбираем переменные с корреляцией > 0.3
    y_columns = integral_correl[
        (abs(integral_correl) > 0.3) &
        (integral_correl.index != 'integrated_index')
    ]
    x_columns_labels = y_columns.index.tolist()
    available_columns = [col for col in x_columns_labels if col in stock_data.columns]

    # Если interval есть в stock_data, добавляем его в обязательном порядке
    if 'interval' in stock_data.columns:
        if 'interval' not in available_columns:
            print("Добавляем interval в обязательном порядке")
            available_columns.append('interval')
        else:
            print("Interval уже есть в отобранных переменных")
    # Если interval нет в stock_data, ничего не добавляем
    # (не выводим сообщение, так как это нормальная ситуация)

    # Убедимся, что все колонки существуют в stock_data
    available_columns = [col for col in available_columns if col in stock_data.columns]

    print(f"Отобрано переменных: {len(available_columns)}")
    print(f"Переменные: {available_columns}")

    return y_columns, stock_data[available_columns]


def get_second_integral_indicators(correl_matrix: pd.DataFrame, stock_data: pd.DataFrame,
                                   first_model_vars: list = None):
    """
    Получаем показатели для второй регрессии с учетом результатов первой модели

    Args:
        correl_matrix: матрица корреляций
        stock_data: данные для анализа
        first_model_vars: ВСЕ переменные, которые были в первой модели (не только значимые)
    """
    integral_correl = correl_matrix['interval'].round(15)

    # КРИТИЧЕСКОЕ ИЗМЕНЕНИЕ: Исключаем ВСЕ переменные, которые были в первой модели
    excluded_vars = first_model_vars if first_model_vars else []

    # ДОБАВЛЯЕМ: исключаем также саму целевую переменную первой модели
    excluded_vars.append('integrated_index')

    print(f"Исключаемые переменные (из первой модели): {excluded_vars}")

    # Отбираем переменные с корреляцией > 0.4 (повышаем порог для большей строгости)
    y_columns = integral_correl[
        (abs(integral_correl) > 0.4) &  # Повышаем порог до 0.4
        (integral_correl.index != 'interval') &
        (~integral_correl.index.isin(excluded_vars))  # ИСКЛЮЧАЕМ все переменные из первой модели
        ]

    x_columns_labels = y_columns.index.tolist()
    available_columns = [col for col in x_columns_labels if col in stock_data.columns]

    print(f"Отобрано переменных для второй регрессии: {len(available_columns)}")
    print(f"Переменные: {available_columns}")

    return y_columns, stock_data[available_columns]


def calc_second_regression(first_model_all_vars=None):
    """
    Вторая регрессионная модель: предсказываем interval на основе других переменных
    с учетом результатов первой модели

    Args:
        first_model_all_vars: ВСЕ переменные, которые были в первой модели (не только значимые)
    """
    db = next(get_db())

    # Получаем данные
    data_records = get_all_data(db)
    years = [record.year for record in data_records]

    from analytics.ryab import get_data as get_mcc_data
    stock_data = get_mcc_data(db, years)

    # Используем ВТОРУЮ матрицу корреляций
    correl_matrix = get_second_correl_matrix(db, years)

    # Получаем коэффициенты и данные для регрессии с учетом первой модели
    coefficients, x_data = get_second_integral_indicators(
        correl_matrix=correl_matrix,
        stock_data=stock_data,
        first_model_vars=first_model_all_vars  # Передаем ВСЕ переменные из первой модели
    )

    # Если после исключения не осталось переменных - выходим
    if x_data.empty or len(x_data.columns) == 0:
        print("Нет подходящих переменных для второй регрессии после исключения!")
        return None, []

    # Получаем реальные значения Y (interval) из базы данных
    y_data = get_y_data_from_db_interval(db, years)

    print("ДАННЫЕ ДЛЯ ВТОРОЙ РЕГРЕССИИ (предсказание interval):")
    print(f"Годы анализа: {years}")
    print(f"\nY переменная (interval из базы): {y_data.values}")
    print(f"\nX переменные (предикторы): {x_data.columns.tolist()}")
    print(f"\nКоэффициенты корреляции с interval:")
    print(coefficients)
    print("\n" + "=" * 60)

    # Проверяем совпадение индексов
    common_years = sorted(list(set(y_data.index).intersection(set(x_data.index))))
    print(f"Общие годы для анализа: {common_years}")
    print(f"Количество наблюдений: {len(common_years)}")

    # Если слишком мало наблюдений - выходим
    if len(common_years) < 3:
        print("Слишком мало наблюдений для регрессионного анализа!")
        return None, []

    # Фильтруем данные по общим годам
    y_data = y_data.loc[common_years]
    x_data = x_data.loc[common_years]

    # Выполняем пошаговое исключение переменных
    final_results, remaining_vars, eliminated_vars = stepwise_t_test_elimination(y_data, x_data)

    if final_results is not None:
        # Выводим результаты финальной модели
        regression_stats, anova_df, coefficients_df, results, y_final, x_final = excel_style_regression(
            y_data, x_data[remaining_vars], add_constant=True, confidence_level=0.95
        )

        print("\nВЫВОД ИТОГОВ ВТОРОЙ РЕГРЕССИОННОЙ МОДЕЛИ")
        print("(предсказание interval)")
        print(" " * 32 + "Регрессионная статистика")
        print(regression_stats.to_string(index=False, header=False))
        print("\n" + " " * 16 + "Дисперсионный анализ")
        print(anova_df.to_string(index=False))
        print("\n" + " " * 8 + "Коэффициенты и статистики")
        print(coefficients_df.to_string(index=False))

        # Уравнение регрессии
        equation = f"interval = {results.params['const']:.6f}"
        for feature in x_final.columns:
            coef = results.params[feature]
            sign = " + " if coef >= 0 else " - "
            equation += f"{sign}{abs(coef):.6f}*{feature}"
        print(f"Уравнение регрессии:\n{equation}")

        print(f"\nR-квадрат: {results.rsquared:.6f}")
        print(f"Скорректированный R-квадрат: {results.rsquared_adj:.6f}")
        print(f"F-статистика: {results.fvalue:.6f} (p-value: {results.f_pvalue:.6f})")

        return results, remaining_vars
    else:
        print("Не удалось построить регрессионную модель!")
        return None, []


def main_analysis_flow():
    """Основной поток анализа с последовательным выполнением моделей"""
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.float_format', '{:.6f}'.format)

    try:
        print("=" * 80)
        print("ШАГ 1: ПЕРВАЯ РЕГРЕССИОННАЯ МОДЕЛЬ (integrated_index)")
        print("=" * 80)

        # Запускаем первую регрессию
        first_model_results = calc_regression()

        if first_model_results and hasattr(first_model_results, 'coefficients'):
            # КРИТИЧЕСКОЕ ИЗМЕНЕНИЕ: получаем ВСЕ переменные из первой модели
            # (не только значимые, а все, что были в исходном наборе)
            db = next(get_db())
            data_records = get_all_data(db)
            years = [record.year for record in data_records]

            from analytics.ryab import get_data as get_mcc_data
            stock_data = get_mcc_data(db, years)
            correl_matrix = get_correl_matrix(db, years)

            # Получаем ВСЕ переменные, которые были в первой модели
            coefficients, x_data_all = get_integral_indicators(
                correl_matrix=correl_matrix,
                stock_data=stock_data
            )

            all_vars_from_first_model = x_data_all.columns.tolist()
            print(f"\nВСЕ переменные из первой модели: {all_vars_from_first_model}")

            print("\n" + "=" * 80)
            print("ШАГ 2: ВТОРАЯ РЕГРЕССИОННАЯ МОДЕЛЬ (interval)")
            print("=" * 80)

            # Запускаем вторую регрессию, передавая ВСЕ переменные из первой
            second_model_results, second_model_vars = calc_second_regression(
                first_model_all_vars=all_vars_from_first_model
            )

            print("\n" + "=" * 80)
            print("ИТОГОВАЯ СИСТЕМА УРАВНЕНИЙ:")
            print("=" * 80)

            if second_model_results:
                print("Система взаимосвязанных уравнений построена успешно!")

        print("\nАнализ завершен успешно!")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

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

    return regression_stats, anova_df, coefficients_df, results, y_data, x_data


def stepwise_t_test_elimination(y_data, x_data):
    """
    Пошаговое исключение переменных на основе t-критерия Стьюдента
    с проверкой F-критерия Фишера на каждом шаге
    """
    n = len(y_data)
    current_x_data = x_data.copy()
    iteration = 1
    eliminated_vars = []

    print("НАЧАЛО ПОШАГОВОГО ИСКЛЮЧЕНИЯ ПЕРЕМЕННЫХ ПО t-КРИТЕРИЮ")
    print("=" * 60)
    print(f"Начальное количество переменных: {len(current_x_data.columns)}")
    print(f"Начальные переменные: {list(current_x_data.columns)}")

    while len(current_x_data.columns) > 0:
        # Выполняем регрессионный анализ с текущим набором переменных
        regression_stats, anova_df, coefficients_df, results, y_current, x_current = excel_style_regression(
            y_data, current_x_data, add_constant=True, confidence_level=0.95
        )

        # Получаем только коэффициенты переменных (без константы)
        var_coefficients = coefficients_df.iloc[1:].copy()

        # Вычисляем степени свободы
        m = len(var_coefficients)  # количество переменных
        d_f = n - m - 1  # n - m - 1 (минус 1 для константы)

        # Получаем критическое значение t-статистики
        if d_f > 0 and d_f <= len(t_criteria_list):
            t_critical = t_criteria_list[d_f - 1]
        else:
            t_critical = 2.0  # консервативное значение для больших выборок

        # Получаем критическое значение F-критерия
        f_critical = get_f_critical(m, d_f)
        f_value = results.fvalue
        f_pvalue = results.f_pvalue

        print(f"\n--- Итерация {iteration} ---")
        print(f"Количество переменных: {m}")
        print(f"Степени свободы (d_f): {d_f}")
        print(f"Критическое значение t-статистики: {t_critical:.4f}")
        print(f"F-статистика: {f_value:.4f}, F-критическое: {f_critical:.4f}, p-value: {f_pvalue:.6f}")

        # Проверяем значимость модели по F-критерию
        if f_value < f_critical:
            print(f"МОДЕЛЬ НЕЗНАЧИМА по F-критерию! (F < F_крит)")
            print("Прекращаем исключение переменных")
            break

        # Находим переменную с наибольшей t-статистикой (по модулю)
        var_coefficients['abs_t'] = var_coefficients['t-статистика']
        max_t_idx = var_coefficients['abs_t'].idxmax()
        max_t_var = var_coefficients.loc[max_t_idx, '']
        max_t_value = var_coefficients.loc[max_t_idx, 'abs_t']
        p_value = var_coefficients.loc[max_t_idx, 'P-Значение']

        # Извлекаем название переменной
        var_name = max_t_var.split('(')[-1].rstrip(')')

        print(f"Переменная с максимальной |t-статистикой|: {var_name} = {max_t_value:.4f}, p = {p_value:.6f}")

        # Проверяем, нужно ли исключать переменную
        if max_t_value > t_critical:
            print(f"ИСКЛЮЧАЕМ {var_name} (|t| = {max_t_value:.4f} > {t_critical:.4f})")
            eliminated_vars.append(var_name)
            current_x_data = current_x_data.drop(columns=[var_name])
            iteration += 1

            # Выводим текущую статистику
            print(f"Оставшиеся переменные: {list(current_x_data.columns)}")
        else:
            print(f"ОСТАВЛЯЕМ {var_name} (|t| = {max_t_value:.4f} <= {t_critical:.4f})")
            print("Все переменные имеют |t-статистику| <= критического значения!")
            break

    # Финальная модель
    if len(current_x_data.columns) > 0:
        print("\n" + "=" * 60)
        print("ФИНАЛЬНАЯ МОДЕЛЬ ПОСЛЕ ИСКЛЮЧЕНИЯ:")
        print(f"Оставшиеся переменные: {list(current_x_data.columns)}")
        print(f"Исключенные переменные: {eliminated_vars}")

        # Проверяем финальную модель по F-критерию
        regression_stats, anova_df, coefficients_df, results, y_final, x_final = excel_style_regression(
            y_data, current_x_data, add_constant=True, confidence_level=0.95
        )

        m_final = len(x_final.columns)
        d_f_final = n - m_final - 1
        f_critical_final = get_f_critical(m_final, d_f_final)
        f_value_final = results.fvalue

        print(f"Проверка финальной модели по F-критерию:")
        print(f"F = {f_value_final:.4f}, F_крит = {f_critical_final:.4f}")

        if f_value_final >= f_critical_final:
            print("Финальная модель ЗНАЧИМА по F-критерию ✓")
        else:
            print("Финальная модель НЕЗНАЧИМА по F-критерию ✗")

        return results, current_x_data.columns.tolist(), eliminated_vars
    else:
        print("Все переменные были исключены из модели!")
        return None, [], x_data.columns.tolist()
def get_y_data_from_db(db, years):
    """Получаем реальные значения integrated_index из базы данных"""
    results = db.query(AnalysisResult).filter(AnalysisResult.year.in_(years)).order_by(AnalysisResult.year).all()

    y_data = pd.Series(
        {result.year: result.integrated_index for result in results},
        name='integrated_index'
    )

    return y_data


def get_y_data_from_db_interval(db, years):
    """Получаем значения interval из базы данных"""
    results = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()

    y_data = pd.Series(
        {result.year: result.interval for result in results},
        name='interval'
    )

    print(f"Y данные (interval) из БД: {y_data.values}")
    return y_data

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

    # Выполняем пошаговое исключение переменных по t-критерию
    final_results, remaining_vars, eliminated_vars = stepwise_t_test_elimination(y_data, x_data)

    if final_results is not None:
        # Выводим результаты финальной модели
        regression_stats, anova_df, coefficients_df, results, y_final, x_final = excel_style_regression(
            y_data, x_data[remaining_vars], add_constant=True, confidence_level=0.95
        )

        print("\nВЫВОД ИТОГОВ ФИНАЛЬНОЙ МОДЕЛИ")
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
        for feature in x_final.columns:
            coef = results.params[feature]
            sign = " + " if coef >= 0 else " - "
            equation += f"{sign}{abs(coef):.6f}*{feature}"
        print(f"Уравнение регрессии:\n{equation}")

        print(f"\nR-квадрат: {results.rsquared:.6f}")
        print(f"Скорректированный R-квадрат: {results.rsquared_adj:.6f}")
        print(f"F-статистика: {results.fvalue:.6f} (p-value: {results.f_pvalue:.6f})")

        coefficients_dict = {
            'const': results.params['const'],
            **{var: results.params[var] for var in remaining_vars}
        }

        print("\nКОЭФФИЦИЕНТЫ ДЛЯ РУЧНОГО РАСЧЕТА:")
        for key, value in coefficients_dict.items():
            print(f"{key}: {value:.6f}")

        # Функция для ручного расчета
        def manual_calculation(values_dict):
            """Ручной расчет с использованием словаря значений"""
            result = coefficients_dict['const']
            for var in remaining_vars:
                if var in values_dict:
                    result += coefficients_dict[var] * values_dict[var]
                else:
                    print(f"Предупреждение: отсутствует {var}")
            return result

        final_results.coefficients = coefficients_dict
        final_results.manual_calculate = manual_calculation

        # Пример
        example_data = {var: 1.0 for var in remaining_vars}
        example_result = manual_calculation(example_data)
        print(f"Пример расчета: {example_result:.4f}")

        return final_results
    else:
        print("Не удалось построить регрессионную модель!")
        return None

if __name__ == "__main__":
    # Запускаем полный анализ
    main_analysis_flow()