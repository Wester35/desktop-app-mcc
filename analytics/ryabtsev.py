import pandas as pd
import numpy as np
from models.data_models import MCKData


class RyabtsevMethod:
    def __init__(self):
        # Названия для отображения
        self.indicator_map = {
            "failures_1": "Отказы 1 категории",
            "failures_2": "Отказы 2 категории",
            "failures_3": "Отказы 3 категории",
            "train_losses": "Поездопотери (поезд/час)",
            "investments": "Кап. вложения (млн руб.)",
            "passengers_daily": "Пассажиры в день",
            "tech_failures": "Технические отказы",
            "fare_cost": "Стоимость проезда (руб.)",
            "interval": "Интервал движения (мин)"
        }

    def get_indicator_name(self, key: str) -> str:
        return self.indicator_map.get(key, key)

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Нормировка показателей:
        - Больше = хуже → обратная нормировка
        - Больше = лучше → прямая нормировка
        """
        norm_df = pd.DataFrame(index=df.index)
        for col in df.columns:
            x_min, x_max = df[col].min(), df[col].max()
            if x_max == x_min:
                # все значения одинаковы
                norm_df[col] = 1.0
                continue
            if col in ["failures_1", "failures_2", "failures_3",
                       "train_losses", "tech_failures", "interval"]:
                norm_df[col] = (x_max - df[col]) / (x_max - x_min)
            else:
                norm_df[col] = (df[col] - x_min) / (x_max - x_min)
        return norm_df

    def calculate_integral_index(self, db, years):
        """Расчёт интегрального показателя по методу Рябцева, с делением на сумму весов"""
        query = (
            db.query(MCKData)
            .filter(MCKData.year.in_(years))
            .order_by(MCKData.year)
            .all()
        )
        if not query:
            return {}, {}

        # создаём DataFrame
        df = pd.DataFrame([{
            "year": row.year,
            "failures_1": row.failures_1,
            "failures_2": row.failures_2,
            "failures_3": row.failures_3,
            "train_losses": row.train_losses,
            "investments": row.investments,
            "passengers_daily": row.passengers_daily,
            "tech_failures": row.tech_failures,
            "fare_cost": row.fare_cost,
            "interval": row.interval,
        } for row in query]).set_index("year")

        # нормировка
        X = self.normalize(df)

        # начальное приближение
        y = X.mean(axis=1)
        weights = {}
        max_iter = 100
        tol = 1e-6

        for _ in range(max_iter):
            corrs = [np.corrcoef(y, X[col])[0, 1] for col in X.columns]
            corrs = np.nan_to_num(corrs)
            w = np.abs(corrs)
            w_sum = np.sum(w)
            if w_sum == 0:
                w = np.ones_like(w) / len(w)
            else:
                w = w / w_sum  # нормируем веса
            y_new = (X * w).sum(axis=1)   # делим на сумму весов

            if np.allclose(y, y_new, atol=tol):
                weights = dict(zip(X.columns, w))
                y = y_new
                break
            y = y_new

        # округление для совпадения с Excel
        y = y.round(4)
        weights = {k: round(v, 4) for k, v in weights.items()}

        results = y.to_dict()
        return results, weights

    def get_interpretation(self, weights: dict) -> str:
        """Текстовое описание результатов"""
        if not weights:
            return "Недостаточно данных для анализа."

        sorted_w = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        text = "Ключевые факторы, влияющие на качество обслуживания:\n\n"
        for key, val in sorted_w:
            text += f"- {self.get_indicator_name(key)}: вес {val:.3f}\n"

        top_factor = sorted_w[0][0]
        text += f"\n⚡ Главный фактор: {self.get_indicator_name(top_factor)}."
        return text
