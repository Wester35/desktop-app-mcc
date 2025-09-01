import numpy as np
from typing import List, Dict
from sqlalchemy.orm import Session


class RyabtsevMethod:
    class RyabtsevMethod:
        def __init__(self):
            self.weights = None

        def normalize_data(self, data: List[float]):
            """Нормирование данных к диапазону 0-1"""
            min_val = min(data)
            max_val = max(data)
            return [(x - min_val) / (max_val - min_val) for x in data]

        def calculate_integral_index(self, db: Session, years: List[int]):
            """Расчет интегрального показателя по методу Рябцева"""
            data_records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()

            if not data_records:
                return None

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

            # Нормируем данные (для отказов - инвертируем, так как меньше = лучше)
            normalized_indicators = {}
            for key, values in indicators.items():
                if key.startswith('failures') or key == 'tech_failures' or key == 'train_losses':
                    # Инвертируем: чем меньше отказов/потерь, тем лучше
                    normalized = self.normalize_data(values)
                    normalized_indicators[key] = [1 - x for x in normalized]
                else:
                    # Для остальных показателей: чем больше, тем лучше
                    normalized_indicators[key] = self.normalize_data(values)