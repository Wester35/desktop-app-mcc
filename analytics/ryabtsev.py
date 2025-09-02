import numpy as np
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from models.data_models import MCKData


class RyabtsevMethod:
    def __init__(self):
        self.normalized = {}
        self.weights = {}
        self.integral_indices = {}

    def normalize(self, data: List[float], positive: bool = True) -> List[float]:
        """Нормирование показателей к диапазону 0-1"""
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            return [0.5 for _ in data]  # константное значение
        normalized = [(x - min_val) / (max_val - min_val) for x in data]
        if not positive:
            normalized = [1 - x for x in normalized]
        return normalized

    def calculate_integral_index(self, db: Session, years: List[int]) -> Tuple[Dict[int, float], Dict[str, float]]:
        """Расчёт интегрального показателя качества услуг методом Рябцева"""
        records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()
        if not records:
            return {}, {}

        # Подготовка данных
        indicators = {
            'fail_1': [],
            'fail_2': [],
            'fail_3': [],
            'train_losses': [],
            'investments': [],
            'passengers': [],
            'tech_failures': [],
            'fare_cost': [],
            'interval': []
        }

        for rec in records:
            indicators['fail_1'].append(rec.failures_1)
            indicators['fail_2'].append(rec.failures_2)
            indicators['fail_3'].append(rec.failures_3)
            indicators['train_losses'].append(rec.train_losses)
            indicators['investments'].append(rec.investments)
            indicators['passengers'].append(rec.passengers_daily)
            indicators['tech_failures'].append(rec.tech_failures)
            indicators['fare_cost'].append(rec.fare_cost)
            indicators['interval'].append(rec.interval)

        # 1. Нормирование
        self.normalized['fail_1'] = self.normalize(indicators['fail_1'], positive=False)
        self.normalized['fail_2'] = self.normalize(indicators['fail_2'], positive=False)
        self.normalized['fail_3'] = self.normalize(indicators['fail_3'], positive=False)
        self.normalized['train_losses'] = self.normalize(indicators['train_losses'], positive=False)
        self.normalized['investments'] = self.normalize(indicators['investments'], positive=True)
        self.normalized['passengers'] = self.normalize(indicators['passengers'], positive=True)
        self.normalized['tech_failures'] = self.normalize(indicators['tech_failures'], positive=False)
        self.normalized['fare_cost'] = self.normalize(indicators['fare_cost'], positive=True)
        self.normalized['interval'] = self.normalize(indicators['interval'], positive=True)

        # 2. Простое среднее
        simple_mean = np.mean(list(self.normalized.values()), axis=0)

        # 3. Начальные веса через корреляцию с простым средним
        weights = {}
        for key, values in self.normalized.items():
            corr = np.corrcoef(values, simple_mean)[0, 1]
            weights[key] = abs(corr) if not np.isnan(corr) else 0.1

        # Нормировка весов
        total_w = sum(weights.values())
        weights = {k: weights[k] / total_w for k in weights}

        # 4. Итерационные этапы 2-5
        integral = simple_mean.copy()
        for _ in range(4):
            # Взвешенная сумма по текущим весам
            integral = np.zeros(len(years))
            for key in self.normalized:
                integral += np.array(self.normalized[key]) * weights[key]

            # Пересчет весов через корреляцию с новым интегральным показателем
            for key, values in self.normalized.items():
                corr = np.corrcoef(values, integral)[0, 1]
                weights[key] = abs(corr) if not np.isnan(corr) else 0.1
            total_w = sum(weights.values())
            weights = {k: weights[k] / total_w for k in weights}

        self.weights = weights
        self.integral_indices = dict(zip([rec.year for rec in records], integral))

        return self.integral_indices, self.weights

    def get_normalized(self) -> Dict[str, List[float]]:
        return self.normalized

    def get_weights(self) -> Dict[str, float]:
        return self.weights
