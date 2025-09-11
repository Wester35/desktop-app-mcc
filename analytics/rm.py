from typing import List
import pandas as pd
import statsmodels.api as sm
from sqlalchemy.orm import Session

from controllers.data_crud import get_all_data
from libs.database import get_db
from models.data_models import MCKData, AnalysisResult
from analytics.constants import t_criteria_list, F_CRITICAL_VALUES
from analytics.corel_matrix import get_data_1, get_data_2, get_correl_matrix, get_second_correl_matrix
import math

def print_corr_significance(corr_with_y: pd.Series, n: int):
    """
    Печать таблицы проверки значимости коэффициентов корреляции.
    """
    dfree = n - 2
    if 1 <= dfree <= len(t_criteria_list):
        t_crit = t_criteria_list[dfree - 1]
    else:
        t_crit = t_criteria_list[-1]

    print("\nПроверка парных коэффициентов корреляции через t-критерий Стьюдента:")
    print("Фактор\t\tr\t\ttфакт\t\ttкр\t\tЗначим?")
    for factor, r in corr_with_y.items():
        if abs(r) >= 0.3:
            t_fact = abs(r) * math.sqrt(dfree) / math.sqrt(1 - r**2)
            is_significant = "Да" if t_fact > t_crit else "Нет"
            print(f"{factor:15s}\t{r:.6f}\t{t_fact:.6f}\t{t_crit:.6f}\t{is_significant}")


def filter_significant_correlations(corr_with_y: pd.Series, n: int) -> list:
    """
    Отбор факторов по корреляции и проверке значимости через t-критерий Стьюдента.
    corr_with_y: Series с коэффициентами корреляции (факторы -> r)
    n: объем выборки (число наблюдений)
    """
    dfree = n - 1 # степени свободы
    if 1 <= dfree <= len(t_criteria_list):
        t_crit = t_criteria_list[dfree - 1]
    else:
        t_crit = t_criteria_list[-1]

    selected = []
    for factor, r in corr_with_y.items():
        if abs(r) >= 0.3:
            # t-фактическое
            t_fact = abs(r) * math.sqrt(dfree) / math.sqrt(1 - r**2)
            if t_fact > t_crit:
                selected.append(factor)
    return selected


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
    """Красивый вывод результата регрессии"""
    print(f"\n=== {name} ===")
    print("Уравнение регрессии:")
    print(format_equation(y_col, result["equation"]))

    print(f"\nКоэффициент детерминации (R²): {result['r2']:.6f}")
    print(f"Fфакт = {result['f_fact']:.6f}, Fкр = {result['f_crit']}")

    if result["f_crit"] is not None:
        if result["f_fact"] > result["f_crit"]:
            print("→ Модель значима (Fфакт > Fкр)")
        else:
            print("→ Модель незначима (Fфакт <= Fкр)")
    else:
        print("⚠️ Fкр не найдено для такой комбинации k1/k2")

    print(f"\nУдалённые факторы: {result['removed']}")
    print(f"Оставшиеся факторы: {result['final_factors']}")

    print("\nКоэффициенты и t-значения:")
    for k in result["equation"].keys():
        coef = result["equation"][k]
        t_val = result["t_values"][k]
        print(f"  {k}: {coef:.6f}, t = {t_val:.6f}")


def build_regression(df: pd.DataFrame, y_col: str, candidate_x: list):
    """Построение модели регрессии"""
    X = sm.add_constant(df[candidate_x])
    y = df[y_col]
    model = sm.OLS(y, X).fit()
    return model


def iterative_regression(df: pd.DataFrame, y_col: str, candidate_x: list):
    """Построение регрессии по методичке: исключение факторов по t-критерию"""
    n = len(df)
    removed = []

    while True:
        model = build_regression(df, y_col, candidate_x)
        m = len(candidate_x)
        dfree = n - m - 1

        # t критическое значение
        if 1 <= dfree <= len(t_criteria_list):
            t_crit = t_criteria_list[dfree - 1]
        else:
            t_crit = t_criteria_list[-1]

        # Проверяем все коэффициенты, кроме const
        t_values = model.tvalues.drop("const")

        # ищем, какие не проходят t-значимость
        insignificant = t_values[abs(t_values) < t_crit].index.tolist()

        if insignificant:
            # удаляем сразу все незначимые факторы
            for factor in insignificant:
                if factor in candidate_x:
                    candidate_x.remove(factor)
                    removed.append(factor)
        else:
            break

    # Проверка по F-критерию Фишера
    f_fact = model.fvalue
    k1 = len(candidate_x)
    k2 = n - k1 - 1
    f_crit = F_CRITICAL_VALUES.get(k1, {}).get(k2, None)

    return {
        "equation": model.params.to_dict(),
        "t_values": model.tvalues.to_dict(),
        "f_fact": f_fact,
        "f_crit": f_crit,
        "r2": model.rsquared,
        "removed": removed,
        "final_factors": candidate_x
    }


def build_integral_model(db: Session, years: List[int]):
    """Модель: интегральный показатель (y)"""
    data = get_data_1(db, years)
    df = pd.DataFrame(data)

    corr_matrix = get_correl_matrix(db, years)
    corr_with_y = corr_matrix["integrated_index"].drop("integrated_index")

    # 🔹 сначала просто фильтр по |r|
    candidates = corr_with_y[abs(corr_with_y) >= 0.3].index.tolist()

    # печатаем таблицу проверки значимости
    print_corr_significance(corr_with_y, len(years))

    y_data = get_y_data_from_db(db, years)
    df["integrated_index"] = y_data.values

    return iterative_regression(df, "integrated_index", candidates)


def build_interval_model(db: Session, years: List[int]):
    """Модель: интервал (y)"""
    data = get_data_2(db, years)
    df = pd.DataFrame(data)

    corr_matrix = get_second_correl_matrix(db, years)
    corr_with_y = corr_matrix["interval"].drop("interval")

    # 🔹 сначала просто фильтр по |r|
    candidates = corr_with_y[abs(corr_with_y) >= 0.3].index.tolist()

    # печатаем таблицу проверки значимости
    print_corr_significance(corr_with_y, len(years))

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

    integral_model = build_integral_model(db, years)
    print_regression_result("Модель интегрального показателя", "integrated_index", integral_model)

    interval_model = build_interval_model(db, years)
    print_regression_result("Модель интервала", "interval", interval_model)

