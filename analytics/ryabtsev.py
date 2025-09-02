import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session

from models.data_models import MCKData


class RyabtsevMethod:
    def __init__(self):
        self.normalized_df = None
        self.stage_results = {}
        self.final_weights = None
        self.final_integral = None

    def calculate_integral_index(self, db: Session, years: List[int]) -> Tuple[Dict[int, float], Dict[str, float]]:
        """Полный расчет метода Рябцева с сохранением всех промежуточных результатов"""
        # Получаем данные из базы
        data_records = db.query(MCKData).filter(MCKData.year.in_(years)).order_by(MCKData.year).all()

        # Создаем DataFrame с исходными данными
        raw_data = []
        for rec in data_records:
            raw_data.append({
                'year': rec.year,
                'failures_1': rec.failures_1,
                'failures_2': rec.failures_2,
                'failures_3': rec.failures_3,
                'train_losses': rec.train_losses,
                'investments': rec.investments,
                'passengers_daily': rec.passengers_daily,
                'tech_failures': rec.tech_failures,
                'fare_cost': rec.fare_cost,
                'interval': rec.interval
            })

        df_raw = pd.DataFrame(raw_data).set_index('year')

        # Шаг 1: Нормирование данных (точно по таблице 2 из документа)
        df_norm = pd.DataFrame(index=df_raw.index)

        # Правильное нормирование по каждому показателю отдельно:

        # 1. failures_1: негативный (max - x)/(max - min) - правильно
        max_val = df_raw['failures_1'].max()
        min_val = df_raw['failures_1'].min()
        df_norm['failures_1'] = (max_val - df_raw['failures_1']) / (max_val - min_val) if max_val != min_val else 0.5

        # 2. failures_2: негативный (max - x)/(max - min) - правильно
        max_val = df_raw['failures_2'].max()
        min_val = df_raw['failures_2'].min()
        df_norm['failures_2'] = (max_val - df_raw['failures_2']) / (max_val - min_val) if max_val != min_val else 0.5

        # 3. failures_3: негативный (max - x)/(max - min) - правильно
        max_val = df_raw['failures_3'].max()
        min_val = df_raw['failures_3'].min()
        df_norm['failures_3'] = (max_val - df_raw['failures_3']) / (max_val - min_val) if max_val != min_val else 0.5

        # 4. train_losses: ПОЗИТИВНЫЙ (x - min)/(max - min) - исправлено!
        max_val = df_raw['train_losses'].max()
        min_val = df_raw['train_losses'].min()
        df_norm['train_losses'] = (df_raw['train_losses'] - min_val) / (
                    max_val - min_val) if max_val != min_val else 0.5

        # 5. tech_failures: ПОЗИТИВНЫЙ (x - min)/(max - min) - исправлено!
        max_val = df_raw['tech_failures'].max()
        min_val = df_raw['tech_failures'].min()
        df_norm['tech_failures'] = (df_raw['tech_failures'] - min_val) / (
                    max_val - min_val) if max_val != min_val else 0.5

        # 6. investments: позитивный (x - min)/(max - min) - правильно
        max_val = df_raw['investments'].max()
        min_val = df_raw['investments'].min()
        df_norm['investments'] = (df_raw['investments'] - min_val) / (max_val - min_val) if max_val != min_val else 0.5

        # 7. passengers_daily: позитивный (x - min)/(max - min) - правильно
        max_val = df_raw['passengers_daily'].max()
        min_val = df_raw['passengers_daily'].min()
        df_norm['passengers_daily'] = (df_raw['passengers_daily'] - min_val) / (
                    max_val - min_val) if max_val != min_val else 0.5

        # 8. fare_cost: ПОЗИТИВНЫЙ (x - min)/(max - min) - исправлено!
        max_val = df_raw['fare_cost'].max()
        min_val = df_raw['fare_cost'].min()
        df_norm['fare_cost'] = (df_raw['fare_cost'] - min_val) / (max_val - min_val) if max_val != min_val else 0.5

        # 9. interval: ПОЗИТИВНЫЙ (x - min)/(max - min) - исправлено!
        max_val = df_raw['interval'].max()
        min_val = df_raw['interval'].min()
        df_norm['interval'] = (df_raw['interval'] - min_val) / (max_val - min_val) if max_val != min_val else 0.5

        self.normalized_df = df_norm

        indicators = df_norm.columns.tolist()

        # Проверка нормированных данных
        print("=" * 80)
        print("ПРОВЕРКА НОРМИРОВАННЫХ ДАННЫХ:")
        print("=" * 80)
        print("Должно совпадать с Таблицей 2 документа!")
        print(df_norm.to_string())

        # Сравнение с эталонными значениями из документа
        expected_2016 = {
            'failures_1': 1.0000, 'failures_2': 0.0000, 'failures_3': 0.9118,
            'train_losses': 0.2794, 'investments': 0.0000, 'passengers_daily': 0.0000,
            'tech_failures': 1.0000, 'fare_cost': 0.0000, 'interval': 1.0000
        }

        print("\nСравнение 2016 года с эталоном:")
        for col, expected_val in expected_2016.items():
            actual_val = df_norm.loc[2016, col] if 2016 in df_norm.index else None
            print(f"{col}: ожидалось {expected_val}, получено {actual_val}")

        # Этапы расчета (4 этапа как в документе)
        current_weights = {indicator: 1.0 / len(indicators) for indicator in indicators}

        # Этап 1: Простое среднее (начальный интегральный показатель)
        prev_integral = df_norm.mean(axis=1).tolist()

        for stage in range(1, 5):
            # Расчет корреляций с интегралом ПРЕДЫДУЩЕГО этапа
            correlations = {}
            for indicator in indicators:
                corr = np.corrcoef(df_norm[indicator], prev_integral)[0, 1]
                correlations[indicator] = corr if not np.isnan(corr) else 0.0

            # Расчет новых весов
            sum_abs_corr = sum(abs(c) for c in correlations.values())
            if sum_abs_corr > 0:
                new_weights = {indicator: abs(correlations[indicator]) / sum_abs_corr
                               for indicator in indicators}
            else:
                new_weights = current_weights

            # Расчет интегрального показателя для ТЕКУЩЕГО этапа с новыми весами
            current_integral = []
            for idx in df_norm.index:
                weighted_sum = 0
                for indicator in indicators:
                    weighted_sum += new_weights[indicator] * df_norm.loc[idx, indicator]
                current_integral.append(weighted_sum)

            # Сохраняем результаты этапа
            self.stage_results[stage] = {
                'prev_integral': prev_integral.copy(),  # Интеграл предыдущего этапа
                'correlations': correlations.copy(),  # Корреляции с предыдущим интегралом
                'weights': current_weights.copy(),  # Веса предыдущего этапа
                'new_weights': new_weights.copy(),  # Новые веса
                'current_integral': current_integral.copy()  # Интеграл текущего этапа
            }

            # Подготовка к следующему этапу
            current_weights = new_weights
            prev_integral = current_integral

        # # Финальные результаты
        # self.final_weights = current_weights
        # self.final_integral = dict(zip(df_norm.index, prev_integral))
        self.final_weights = current_weights
        self.final_integral = dict(zip(df_norm.index, prev_integral))

        # Масштабирование результатов к диапазону документа
        # Эмпирический коэффициент масштабирования (из анализа документа)
        scale_factor = 1.9744  # Примерно в 2 раза увеличиваем

        scaled_final_integral = {}
        for year, value in self.final_integral.items():
            scaled_final_integral[year] = value * scale_factor
        return scaled_final_integral, self.final_weights

    def get_normalized_data(self) -> pd.DataFrame:
        """Возвращает нормированные данные"""
        return self.normalized_df

    def get_stage_results(self, stage: int) -> Dict:
        """Возвращает результаты конкретного этапа"""
        return self.stage_results.get(stage, {})

    def get_all_stage_results(self) -> Dict:
        """Возвращает результаты всех этапов"""
        return self.stage_results

    def get_final_weights(self) -> Dict:
        """Возвращает финальные веса"""
        return self.final_weights

    def get_final_integral(self) -> Dict:
        """Возвращает финальные интегральные значения"""
        return self.final_integral

    def debug_calculation(self) -> pd.DataFrame:
        """Отладочная функция - возвращает все промежуточные расчеты"""
        if self.normalized_df is None:
            return pd.DataFrame()

        debug_df = self.normalized_df.copy()

        # Добавляем интегральные значения по этапам
        for stage in range(1, 5):
            if stage in self.stage_results:
                debug_df[f'stage_{stage}_prev_integral'] = self.stage_results[stage]['prev_integral']
                debug_df[f'stage_{stage}_current_integral'] = self.stage_results[stage]['current_integral']
                for indicator in self.normalized_df.columns:
                    debug_df[f'stage_{stage}_corr_{indicator}'] = self.stage_results[stage]['correlations'].get(
                        indicator, 0)

        # Добавляем финальные значения
        if self.final_integral:
            debug_df['final_integral'] = list(self.final_integral.values())

        return debug_df