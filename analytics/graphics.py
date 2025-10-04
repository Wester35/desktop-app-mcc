import pickle
import matplotlib.pyplot as plt
import scipy.stats as stats
import mplcursors
from pathlib import Path

def plot_regression_diagnostics(pkl_name: str):
    with open(Path(__file__).parent.parent.absolute() / str("data/" + pkl_name + ".pkl"), "rb") as f:
        result_dict = pickle.load(f)

    model = result_dict["model"]

    y_true = model.model.endog
    y_pred = model.fittedvalues
    residuals = model.resid
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # === Predicted vs Observed ===
    scatter = axes[0].scatter(y_pred, y_true, color="blue", label="Данные")
    axes[0].plot(
        [min(y_pred) - 0.15, max(y_pred) + 0.15],
        [min(y_pred) - 0.15, max(y_pred) + 0.15],
        "r-", label="y = ŷ"
    )
    axes[0].set_xlabel("Predicted Values")
    axes[0].set_ylabel("Observed Values")
    axes[0].set_title("Predicted vs. Observed")
    axes[0].legend()
    axes[0].grid(True)

    cursor1 = mplcursors.cursor(scatter, hover=True)
    @cursor1.connect("add")
    def on_add(sel):
        idx = sel.index
        sel.annotation.set_text(
            f"Observed={y_true[idx]:.4f}\nPredicted={y_pred[idx]:.4f}"
        )

    (osm, osr), (slope, intercept, r) = stats.probplot(residuals, dist="norm")
    scatter2 = axes[1].scatter(osm, osr, color="green", label="Residuals")
    axes[1].plot(osm, slope * osm + intercept, "r-", label="Нормальное распределение")
    axes[1].set_title("Normal Probability Plot of Residuals")
    axes[1].set_xlabel("Theoretical Quantiles")
    axes[1].set_ylabel("Ordered Residuals")
    axes[1].legend()
    axes[1].grid(True)

    cursor2 = mplcursors.cursor(scatter2, hover=True)

    @cursor2.connect("add")
    def on_add2(sel):
        idx = sel.index
        sel.annotation.set_text(
            f"Theor.Q={osm[idx]:.4f}\nResid={osr[idx]:.4f}"
        )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_regression_diagnostics("interval")
