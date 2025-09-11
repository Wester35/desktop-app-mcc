from numpy.ma.extras import average
from sqlalchemy.orm import Session
from controllers.data_crud import get_all_data


def predict_prokofiev(db: Session):
    try:
        data = get_all_data(db)
        years = [record.year for record in data]
        y1, y2, y3, y4, y5 = years[-5:]

        abs_pr_12 = y2 - y1
        abs_pr_24 = y4 - y2
        abs_pr_34 = y4 - y3
        abs_pr_45 = y5 - y4
        abs_pr_35 = y5 - y3
        abs_pr_25 = y5 - y2
        abs_pr_23 = y3 - y2

        avg_abs_pr_13 = (y3 - y1) / 2
        avg_abs_pr_23 = (avg_abs_pr_13 + abs_pr_23) / 2
        avg_abs_pr_14 = (y4 - y1) / 3
        avg_abs_pr_24 = (y4 - y2) / 2
        avg_abs_pr_34 = (avg_abs_pr_14 + avg_abs_pr_24 + abs_pr_34) / 3
        avg_abs_pr_15 = (y5 - y1) / 4
        avg_abs_pr_25 = (y5 - y2) / 3
        avg_abs_pr_35 = (y5 - y3) / 2
        avg_abs_pr_45 = (avg_abs_pr_15 + avg_abs_pr_25 + avg_abs_pr_35 + abs_pr_45) / 4

        alignment_3 = average()
        alignment_2 =
        alignment_1 =
        alignment_4 =
        alignment_5 =
    except Exception as e:
        print(e)