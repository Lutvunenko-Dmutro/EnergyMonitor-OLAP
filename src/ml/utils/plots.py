import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.metrics import r2_score

def generate_final_plots(actual, lstm_pred, arima_pred, results_dir):
    """Generates 3 standard DS-style plots for model evaluation."""
    sns.set_theme(style="whitegrid", palette="muted")
    
    # 1. Comparison Plot
    plt.figure(figsize=(15, 6))
    plt.plot(actual[:336], label='Actual Load', color='#ff9f43', linewidth=2.5, alpha=0.8)
    plt.plot(lstm_pred[:336], label='LSTM Forecast', color='#ee5253', linewidth=2.5, alpha=0.9)
    plt.plot(arima_pred[:336], label='ARIMA Forecast', color='#10ac84', linewidth=2, linestyle='--', alpha=0.8)
    plt.title('Comparison of forecasts with actual values (14 Days)', fontsize=14, fontweight='bold')
    plt.legend()
    plt.savefig(f"{results_dir}/fig_comparison.png", dpi=300)
    plt.close()

    # 2. Error Distribution
    lstm_errors = actual[:336] - lstm_pred[:336]
    plt.figure(figsize=(10, 6))
    sns.histplot(lstm_errors, bins=40, stat="density", color='#5f27cd', alpha=0.4, label='LSTM Errors')
    mu_l, std_l = norm.fit(lstm_errors)
    x_l = np.linspace(min(lstm_errors), max(lstm_errors), 100)
    plt.plot(x_l, norm.pdf(x_l, mu_l, std_l), color='#ee5253', linewidth=2.5, label=f'Fit: mu={mu_l:.2f}')
    plt.title('Error Distribution Distribution')
    plt.legend()
    plt.savefig(f"{results_dir}/fig_errors.png", dpi=300)
    plt.close()

    # 3. Scatter Plot
    r2 = r2_score(actual[:336], lstm_pred[:336])
    plt.figure(figsize=(8, 8))
    plt.scatter(actual[:336], lstm_pred[:336], color='#54a0ff', alpha=0.7, s=50)
    lims = [min(actual[:336]), max(actual[:336])]
    plt.plot(lims, lims, color='#ee5253', linestyle='--')
    plt.title(f'Scatter Plot (R2 = {r2:.4f})')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(f"{results_dir}/fig_scatter.png", dpi=300)
    plt.close()
