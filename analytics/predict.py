from sqlalchemy.orm import Session

from analytics.reg import build_interval_model
from analytics.prokofiev import predict_prokofiev
from libs.database import get_db


def calculate_final_predict(db: Session):
    from controllers.data_crud import get_all_data
    data = get_all_data(db)
    years = [record.year for record in data]
    interval_model = build_interval_model(db, years)

    equation_names = [key for key in interval_model['equation'].keys() if key != 'const']

    res_name = []
    for name in equation_names:
        result = predict_prokofiev(db, str(name))
        res_name.append(result)


    final_prediction = interval_model['equation']['const']

    for i, name in enumerate(equation_names):
        coefficient = interval_model['equation'][name]
        prediction = res_name[i]
        final_prediction += coefficient * prediction

    print(f"Final prediction: {final_prediction:.6f}")

    return final_prediction

if __name__ == "__main__":
    db = next(get_db())
    calculate_final_predict(db)