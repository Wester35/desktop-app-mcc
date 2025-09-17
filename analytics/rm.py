from typing import List
import pandas as pd
import statsmodels.api as sm
from sqlalchemy.orm import Session

from controllers.data_crud import get_all_data
from libs.database import get_db
from models.data_models import MCKData, AnalysisResult
from analytics.constants import t_criteria_list, F_CRITICAL_VALUES
from analytics.corel_matrix import get_data_1, get_data_2, get_correl_matrix, get_second_correl_matrix


def format_equation(y_col: str, equation: dict) -> str:
    """Форматирование уравнения регрессии в виде строки"""
    terms = []
    for k, v in equation.items():
        if k == "const":
            const = round(v, 6)
        else:
            coef = round(v, 6)
            sign = "+" if coef >= 0 else "-"
            terms.append(f" {sign} {abs(coef)}*{k}")
    return f"{y_col} = {round(const, 6)}" + "".join(terms)


def print_regression_result(name: str, y_col: str, result: dict):
    """Красивый вывод результата регрессии (обновлённая версия)"""
    print(f"\n{'=' * 50}")
    print(f"=== {name} ===")
    print(f"{'=' * 50}")

    print("Уравнение регрессии:")
    print(format_equation(y_col, result["equation"]))

    print(f"\nКоэффициент детерминации (R²): {result['r2']:.6f}")
    print(f"Скорректированный R²: {result['adj_r2']:.6f}")
    print(f"Fфакт = {result['f_fact']:.6f}, Fкр = {result['f_crit']}")

    if result["f_crit"] is not None:
        if result["f_fact"] > result["f_crit"]:
            print("→ Модель значима (Fфакт > Fкр)")
        else:
            print("→ Модель незначима (Fфакт <= Fкр)")
    else:
        print("⚠️ Fкр не найдено для такой комбинации k1/k2")

    print(f"\nМетод исключения: {'p-value' if result['use_pvalue'] else 't-статистика'}")
    print(f"Уровень значимости: {result['alpha']}")
    print(f"Удалённые факторы: {result['removed']}")
    print(f"Оставшиеся факторы: {result['final_factors']}")

    print("\nДетальная статистика коэффициентов:")
    print(f"{'Фактор':<15} {'Коэффициент':<15} {'t-значение':<15} {'p-value':<15} {'Значим'}")
    print("-" * 75)

    for factor in result["equation"].keys():
        coef = result["equation"][factor]
        t_val = result["t_values"][factor]
        p_val = result["p_values"][factor]
        significant = p_val <= result["alpha"] if factor != "const" else "N/A"

        print(f"{factor:<15} {coef:<15.6f} {t_val:<15.6f} {p_val:<15.6f} {significant}")


def build_regression(df: pd.DataFrame, y_col: str, candidate_x: list):
    """Построение модели регрессии"""
    X = sm.add_constant(df[candidate_x])
    y = df[y_col]
    model = sm.OLS(y, X).fit()
    return model


def iterative_regression(df: pd.DataFrame, y_col: str, candidate_x: list, alpha: float = 0.05, use_pvalue: bool = True):
    """
    Итеративное исключение факторов по t-критерию или p-value

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame с данными
    y_col : str
        Название зависимой переменной
    candidate_x : list
        Список кандидатов-предикторов
    alpha : float
        Уровень значимости (по умолчанию 0.05)
    use_pvalue : bool
        Если True - использует p-value для исключения,
        если False - использует t-статистику
    """
    n = len(df)
    removed = []
    iteration = 0

    print(f"Начальный набор факторов: {candidate_x}")
    if use_pvalue:
        print("Критерий исключения: p-value >", alpha)
    else:
        print("Критерий исключения: |t| < t_critical")

    while candidate_x and iteration < 50:  # Защита от бесконечного цикла
        iteration += 1
        model = build_regression(df, y_col, candidate_x)
        m = len(candidate_x)
        dfree = n - m - 1

        # Получаем статистику коэффициентов (исключая константу)
        results = []
        for factor in candidate_x:
            if use_pvalue:
                # Критерий по p-value
                p_value = model.pvalues[factor]
                is_significant = p_value <= alpha
                results.append((factor, p_value, is_significant))
            else:
                # Критерий по t-статистике
                t_value = model.tvalues[factor]
                if 1 <= dfree <= len(t_criteria_list):
                    t_crit = t_criteria_list[dfree - 1]
                else:
                    t_crit = t_criteria_list[-1]
                is_significant = abs(t_value) >= t_crit
                results.append((factor, t_value, is_significant))

        # Находим наименее значимый фактор
        if use_pvalue:
            # Для p-value ищем наибольшее значение (наименее значимый)
            weakest_factor = max(results, key=lambda x: x[1])[0]
            weakest_value = max(results, key=lambda x: x[1])[1]
        else:
            # Для t-статистики ищем наименьшее абсолютное значение
            weakest_factor = min(results, key=lambda x: abs(x[1]))[0]
            weakest_value = min(results, key=lambda x: abs(x[1]))[1]

        # Проверяем, нужно ли исключать самый слабый фактор
        if use_pvalue:
            should_remove = weakest_value > alpha
        else:
            should_remove = abs(weakest_value) < t_crit

        if should_remove:
            candidate_x.remove(weakest_factor)
            removed.append(weakest_factor)
            print(f"Итерация {iteration}: удалён {weakest_factor} "
                  f"({'p-value' if use_pvalue else 't-value'} = {weakest_value:.6f})")
        else:
            print(f"Итерация {iteration}: все факторы значимы")
            break

    # Финальная модель
    final_model = build_regression(df, y_col, candidate_x)
    k1 = len(candidate_x)
    k2 = n - k1 - 1
    f_crit = F_CRITICAL_VALUES.get(k1, {}).get(k2, None)

    return {
        "equation": final_model.params.to_dict(),
        "t_values": final_model.tvalues.to_dict(),
        "p_values": final_model.pvalues.to_dict(),
        "f_fact": final_model.fvalue,
        "f_crit": f_crit,
        "r2": final_model.rsquared,
        "adj_r2": final_model.rsquared_adj,
        "removed": removed,
        "final_factors": candidate_x,
        "use_pvalue": use_pvalue,
        "alpha": alpha
    }


def build_integral_model(db: Session, years: List[int], use_pvalue: bool = True):
    """Модель: интегральный показатель (y) с выбором метода"""
    data = get_data_1(db, years)
    df = pd.DataFrame(data)

    corr_matrix = get_correl_matrix(db, years)
    corr_with_y = corr_matrix["integrated_index"].drop("integrated_index")
    candidates = corr_with_y[abs(corr_with_y) >= 0.199].index.tolist()

    y_data = get_y_data_from_db(db, years)
    df["integrated_index"] = y_data.values

    return iterative_regression(df, "integrated_index", candidates, use_pvalue=use_pvalue)


def build_interval_model(db: Session, years: List[int]):
    """Модель: интервал (y)"""
    data = get_data_2(db, years)
    df = pd.DataFrame(data)

    corr_matrix = get_second_correl_matrix(db, years)
    corr_with_y = corr_matrix["interval"].drop("interval")
    candidates = corr_with_y[abs(corr_with_y) >= 0.2].index.tolist()

    y_data = get_y_data_from_db_interval(db, years)
    df["interval"] = y_data.values

    return iterative_regression(df, "interval", candidates)

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

if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.float_format', '{:.6f}'.format)
    db = next(get_db())
    data_records = get_all_data(db)
    years = [record.year for record in data_records]

    integral_model_pvalue = build_integral_model(db, years, use_pvalue=True)
    print_regression_result("Модель интегрального показателя (p-value)", "integrated_index", integral_model_pvalue)

    integral_model_tstat = build_integral_model(db, years, use_pvalue=False)
    print_regression_result("Модель интегрального показателя (t-stat)", "integrated_index", integral_model_tstat)

    interval_model = build_interval_model(db, years)
    print_regression_result("Модель интервала", "interval", interval_model)

