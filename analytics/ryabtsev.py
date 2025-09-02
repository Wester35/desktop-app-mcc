import numpy as np
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from models.data_models import MCKData


class RyabtsevMethod:
    def __init__(self):
        self.weights = None
        self.normalized_indicators = None

    def normalize_data(self, data: List[float], invert: bool = False) -> List[float]:
        """Нормирование данных к диапазону 0-1 с возможностью инверсии"""
        if not data:
            return []

        min_val = min(data)
        max_val = max(data)

        if max_val == min_val:
            normalized = [0.5 for _ in data]  # нейтральное значение
        else:
            normalized = [(x - min_val) / (max_val - min_val) for x in data]

        if invert:
            normalized = [1 - x for x in normalized]

        return normalized

    def calculate_integral_index(self, db: Session, years: List[int]) -> Tuple[Dict[int, float], Dict[str, float]]:
        """Расчет интегрального показателя по методу Рябцева (имитация Excel)"""
        data_records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()
        if not data_records:
            return {}, {}

        indicators = {
            'failures_1': [],
            'failures_2': [],
            'failures_3': [],
            'train_losses': [],
            'investments': [],
            'passengers_daily': [],
            'tech_failures': [],
            'fare_cost': [],
        }

        years_list = []
        for rec in data_records:
            years_list.append(rec.year)
            indicators['failures_1'].append(rec.failures_1)
            indicators['failures_2'].append(rec.failures_2)
            indicators['failures_3'].append(rec.failures_3)
            indicators['train_losses'].append(rec.train_losses)
            indicators['investments'].append(rec.investments)
            indicators['passengers_daily'].append(rec.passengers_daily)
            indicators['tech_failures'].append(rec.tech_failures)
            indicators['fare_cost'].append(rec.fare_cost)

        # Нормируем показатели
        self.normalized_indicators = {}
        negative_keys = ['failures_1', 'failures_2', 'failures_3', 'train_losses', 'tech_failures']
        positive_keys = ['investments', 'passengers_daily', 'fare_cost']

        for key in negative_keys:
            self.normalized_indicators[key] = self.normalize_data(indicators[key], invert=True)
        for key in positive_keys:
            self.normalized_indicators[key] = self.normalize_data(indicators[key], invert=False)

        # Этапы расчета интегрального показателя
        weights = {key: 1.0 for key in self.normalized_indicators}  # начальные веса = 1
        integral_values = None

        for stage in range(5):  # 5 этапов
            # считаем взвешенную сумму
            integral_values = []
            for i in range(len(years_list)):
                s = sum(weights[k] * self.normalized_indicators[k][i] for k in weights)
                integral_values.append(s)

            # пересчет весов на основе корреляции с текущим интегральным показателем
            new_weights = {}
            for k in weights:
                corr = np.corrcoef(self.normalized_indicators[k], integral_values)[0, 1]
                new_weights[k] = abs(corr) if not np.isnan(corr) else 0.0
            weights = new_weights  # берем абсолютные корреляции как новые веса, без нормирования

        self.weights = weights

        # Финальная взвешенная сумма — интегральный показатель
        final_indices = []
        for i in range(len(years_list)):
            s = sum(weights[k] * self.normalized_indicators[k][i] for k in weights)
            final_indices.append(s)

        return dict(zip(years_list, final_indices)), weights

    def get_normalized_data(self) -> Dict[str, List[float]]:
        return self.normalized_indicators or {}

    def get_weights(self) -> Dict[str, float]:
        return self.weights or {}
