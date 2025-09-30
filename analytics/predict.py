from sqlalchemy.orm import Session

from analytics.equations import build_interval_model, build_integral_model
from analytics.prokofiev import predict_prokofiev
from libs.database import get_db


def calculate_final_predict(db: Session, dict):
    equation_names = [key for key in dict['equation'].keys() if key != 'const']

    res_name = []
    for name in equation_names:
        result = predict_prokofiev(db, str(name))
        res_name.append(result)


    final_prediction = dict['equation']['const']

    for i, name in enumerate(equation_names):
        coefficient = dict['equation'][name]
        prediction = res_name[i]
        final_prediction += coefficient * prediction

    print(f"Final prediction: {final_prediction:.6f}")

    return final_prediction

def calculate_final_predict_integral(db: Session, dict):

    equation_names = [key for key in dict['equation'].keys() if key != 'const']

    res_name = []
    for name in equation_names:
        result = predict_prokofiev(db, str(name))
        res_name.append(result)


    final_prediction = dict['equation']['const']

    for i, name in enumerate(equation_names):
        coefficient = dict['equation'][name]
        prediction = res_name[i]
        final_prediction += coefficient * prediction

    print(f"Final prediction: {final_prediction:.6f}")

    return final_prediction

if __name__ == "__main__":
    db = next(get_db())
    calculate_final_predict(db)
    calculate_final_predict_integral(db)
