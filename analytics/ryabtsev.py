import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session

from models.data_models import MCKData


class RyabtsevMethod:
    def __init__(self):
        self.normalized_df = None
        self.stage_results = {}
        self.final_weights = None
        self.final_integral = None
        self.raw_data_df = None

    def calculate_weights_for_stage(self, stage: int) -> Optional[Dict[str, float]]:
        """
        Расчет отдельных весов для конкретного этапа по формуле:
        вес = коэффициент корреляции этого этапа / сумма коэффициентов корреляций этого этапа

        Parameters:
        -----------
        stage : int
            Номер этапа (от 1 до 4)

        Returns:
        --------
        Dict[str, float] or None
            Словарь с весами показателей для указанного этапа
        """
        if stage not in self.stage_results:
            return None

        stage_data = self.stage_results[stage]
        correlations = stage_data['correlations']

        # Сумма абсолютных значений корреляций
        sum_abs_corr = sum(abs(corr) for corr in correlations.values())

        if sum_abs_corr == 0:
            return None

        # Расчет весов по формуле
        weights = {}
        for indicator, corr in correlations.items():
            weights[indicator] = abs(corr) / sum_abs_corr

        return weights

    def get_all_stage_weights(self) -> Dict[int, Dict[str, float]]:
        """
        Возвращает веса для всех этапов расчета

        Returns:
        --------
        Dict[int, Dict[str, float]]
            Словарь, где ключ - номер этапа, значение - словарь весов
        """
        all_weights = {}

        for stage in range(1, 5):
            stage_weights = self.calculate_weights_for_stage(stage)
            if stage_weights:
                all_weights[stage] = stage_weights

        return all_weights

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
        self.raw_data_df = df_raw.copy()

        # Шаг 1: Нормирование данных
        # df_norm = pd.DataFrame(index=df_raw.index)
        from analytics.ryab import normalize_data as nd
        df_norm = nd(self.raw_data_df)

        indicators = df_norm.columns.tolist()

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

            # Расчет новых весов по формуле: |корреляция| / сумма(|корреляций|)
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
                'prev_integral': prev_integral.copy(),
                'correlations': correlations.copy(),
                'weights': current_weights.copy(),
                'new_weights': new_weights.copy(),
                'current_integral': current_integral.copy()
            }

            # Подготовка к следующему этапу
            current_weights = new_weights
            prev_integral = current_integral

        # Финальные результаты
        self.final_weights = current_weights
        self.final_integral = dict(zip(df_norm.index, prev_integral))

        # Масштабирование результатов
        scale_factor = 1.9744
        scale_factor_w = 2
        scaled_final_integral = {}
        for year, value in self.final_integral.items():
            scaled_final_integral[year] = value * scale_factor
        scaled_final_weights = {}
        for indicator, weight in self.final_weights.items():
            scaled_final_weights[indicator] = weight * scale_factor_w

        return scaled_final_integral, scaled_final_weights

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

    def get_raw_data(self) -> pd.DataFrame:
        """Возвращает исходные данные"""
        return self.raw_data_df

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