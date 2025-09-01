import numpy as np
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from models.data_models import MCKData


class RyabtsevMethod:
    def __init__(self):
        self.weights = None
        self.normalized_indicators = None

    def normalize_data(self, data: List[float], invert: bool = False):
        """Нормирование данных к диапазону 0-1 с возможностью инверсии"""
        if not data:
            return []

        min_val = min(data)
        max_val = max(data)

        # Избегаем деления на ноль
        if max_val == min_val:
            normalized = [0.5 for _ in data]  # neutral value
        else:
            normalized = [(x - min_val) / (max_val - min_val) for x in data]

        if invert:
            normalized = [1 - x for x in normalized]

        return normalized

    def calculate_integral_index(self, db: Session, years: List[int]) -> Tuple[Dict[int, float], Dict[str, float]]:
        """Расчет интегрального показателя по методу Рябцева"""
        # Получаем данные за указанные годы
        data_records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()

        if not data_records:
            return {}, {}

        # Подготавливаем данные для расчета
        indicators = {
            'failures_1': [],
            'failures_2': [],
            'failures_3': [],
            'train_losses': [],
            'investments': [],
            'passengers_daily': [],
            'tech_failures': [],
            'fare_cost': []
        }

        years_list = []
        for record in data_records:
            years_list.append(record.year)
            indicators['failures_1'].append(record.failures_1)
            indicators['failures_2'].append(record.failures_2)
            indicators['failures_3'].append(record.failures_3)
            indicators['train_losses'].append(record.train_losses)
            indicators['investments'].append(record.investments)
            indicators['passengers_daily'].append(record.passengers_daily)
            indicators['tech_failures'].append(record.tech_failures)
            indicators['fare_cost'].append(record.fare_cost)

        # Нормируем данные с учетом направленности показателей
        self.normalized_indicators = {}

        # Показатели где МЕНЬШЕ = ЛУЧШЕ (инвертируем)
        for key in ['failures_1', 'failures_2', 'failures_3', 'tech_failures', 'train_losses']:
            self.normalized_indicators[key] = self.normalize_data(indicators[key], invert=True)

        # Показатели где БОЛЬШЕ = ЛУЧШЕ
        for key in ['investments', 'passengers_daily']:
            self.normalized_indicators[key] = self.normalize_data(indicators[key], invert=False)

        # Для стоимости проезда - нейтральный показатель (меньше = лучше для пассажиров, но может быть хуже для доходов)
        self.normalized_indicators['fare_cost'] = self.normalize_data(indicators['fare_cost'], invert=False)

        # Итерационный расчет весов (4 итерации)
        n_indicators = len(self.normalized_indicators)
        weights = {key: 1 / n_indicators for key in self.normalized_indicators.keys()}

        for iteration in range(4):
            # Расчет средних значений для каждого года
            yearly_means = []
            for i in range(len(years_list)):
                weighted_sum = sum(weights[key] * self.normalized_indicators[key][i]
                                   for key in weights.keys())
                yearly_means.append(weighted_sum)

            # Пересчет весов на основе корреляции
            new_weights = {}
            for key in weights.keys():
                indicator_values = self.normalized_indicators[key]
                if len(set(indicator_values)) > 1:  # Проверяем что есть вариация
                    correlation = np.corrcoef(indicator_values, yearly_means)[0, 1]
                    if np.isnan(correlation):
                        correlation = 0
                    new_weights[key] = abs(correlation)
                else:
                    new_weights[key] = 0.1  # Минимальный вес для константных показателей

            # Нормируем веса чтобы сумма = 1
            total = sum(new_weights.values())
            if total > 0:
                weights = {key: new_weights[key] / total for key in new_weights.keys()}
            else:
                # Если все корреляции нулевые, используем равные веса
                weights = {key: 1 / n_indicators for key in new_weights.keys()}

        self.weights = weights

        # Расчет итогового интегрального показателя
        integral_indices = []
        for i in range(len(years_list)):
            integral_index = sum(weights[key] * self.normalized_indicators[key][i]
                                 for key in weights.keys())
            integral_indices.append(integral_index)

        # Масштабируем к диапазону 0-100 для удобства
        max_index = max(integral_indices) if integral_indices else 1
        scaled_indices = [index * 100 / max_index for index in integral_indices] if max_index > 0 else integral_indices

        return dict(zip(years_list, scaled_indices)), weights

    def get_normalized_data(self) -> Dict[str, List[float]]:
        """Получение нормированных данных"""
        return self.normalized_indicators or {}

    def get_weights(self) -> Dict[str, float]:
        """Получение весов показателей"""
        return self.weights or {}