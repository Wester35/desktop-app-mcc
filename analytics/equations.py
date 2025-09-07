import pandas as pd

from analytics.corel_matrix import get_correl_matrix
from libs.database import get_db


def get_indicators(correl_matrix: pd.DataFrame):
    integral_correl = correl_matrix['integrated_index'].round(15)
    filtered = integral_correl[abs(integral_correl) > 0.19]
    return filtered


if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None) 
    pd.set_option('display.float_format', '{:.15f}'.format)
    db = next(get_db())
    from controllers.data_crud import get_all_data
    data = get_all_data(db)
    years = [record.year for record in data]

    print(get_indicators(get_correl_matrix(db, years)))