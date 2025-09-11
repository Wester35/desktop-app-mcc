from sqlalchemy.orm import Session
from controllers.data_crud import get_all_data
from libs.database import get_db


def predict_prokofiev(db: Session, index = ""):
    try:
        data = get_all_data(db)
        if not data or len(data) < 5:
            return []

        last_five_records = data[-5:]
        if not hasattr(last_five_records[0], index):
            return []

        last_five_years_data = [getattr(record, index) for record in last_five_records]
        y1, y2, y3, y4, y5 = last_five_years_data

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
        avg_abs_pr_24 = abs_pr_24 / 2
        avg_abs_pr_34 = (avg_abs_pr_14 + avg_abs_pr_24 + abs_pr_34) / 3
        avg_abs_pr_15 = (y5 - y1) / 4
        avg_abs_pr_25 = abs_pr_25 / 3
        avg_abs_pr_35 = abs_pr_35 / 2
        avg_abs_pr_45 = (avg_abs_pr_15 + avg_abs_pr_25 + avg_abs_pr_35 + abs_pr_45) / 4

        alignment_3 = (y1 + y2 + y3 + y4 + y5) / 5
        alignment_2 = alignment_3 - avg_abs_pr_23
        alignment_1 = alignment_2 - abs_pr_12
        alignment_4 = alignment_3 + avg_abs_pr_34
        alignment_5 = alignment_4 + avg_abs_pr_45

        predict = alignment_5 + avg_abs_pr_45

        return predict

    except Exception as e:
        print(e)

if __name__ == "__main__":
    db = next(get_db())

    print(predict_prokofiev(db, "fare_cost"))