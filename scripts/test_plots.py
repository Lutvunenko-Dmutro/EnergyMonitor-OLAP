import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# ==========================================
# 1. ГРАФІК РОЗПОДІЛУ ПОХИБОК (ЛІВИЙ)
# ==========================================
def plot_error_distribution(errors_lstm, errors_arima, mu_lstm, std_lstm, mu_arima, std_arima, version="v1"):
    fig, ax = plt.subplots(figsize=(9, 6), facecolor='white')
    ax.set_facecolor('white')

    # Гістограми з ЧОРНОЮ обвідкою (edgecolor='black')
    ax.hist(errors_lstm, bins=40, density=True, alpha=0.5, color='purple', edgecolor='black', linewidth=0.5, label='LSTM Errors')
    ax.hist(errors_arima, bins=40, density=True, alpha=0.4, color='forestgreen', edgecolor='black', linewidth=0.5, label='ARIMA Errors')

    # Генерація кривих Гауса
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p_lstm = stats.norm.pdf(x, mu_lstm, std_lstm)
    p_arima = stats.norm.pdf(x, mu_arima, std_arima)

    # Лінії Гауса (червона та зелена пунктирні)
    ax.plot(x, p_lstm, color='red', linestyle='--', linewidth=2, 
            label=f'LSTM Gauss\n' + rf'$\mu={mu_lstm:.2f}, \sigma={std_lstm:.2f}$')
    ax.plot(x, p_arima, color='green', linestyle='--', linewidth=2, 
            label=f'ARIMA Gauss\n' + rf'$\mu={mu_arima:.2f}, \sigma={std_arima:.2f}$')

    # Оформлення
    ax.set_title(f'Normal distribution of forecast errors (LSTM vs ARIMA - {version})', color='black')
    ax.set_xlabel('Похибка (МВт)', color='black')
    ax.set_ylabel('Густина', color='black')
    ax.tick_params(colors='black')
    ax.grid(True, linestyle='-', alpha=0.3, color='gray') # Легка сітка
    ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='lightgray')

    plt.tight_layout()
    plt.savefig(f"lstm_error_dist_{version}_test.png", dpi=300, bbox_inches='tight')
    plt.close()

# ==========================================
# 2. ГРАФІК ПОРІВНЯННЯ ТРЕНДІВ (ПРАВИЙ)
# ==========================================
def plot_forecast_comparison(timestamps, actual_load, lstm_pred, arima_pred, rmse_lstm, rmse_arima, version="v1"):
    fig, ax = plt.subplots(figsize=(11, 6), facecolor='white')
    ax.set_facecolor('white')

    # 1. Фактичні дані (Темно-сіра тонка лінія)
    ax.plot(timestamps, actual_load, color='#404040', linewidth=1.2, label='Фактичні дані (Real)')
    
    # 2. Прогноз ARIMA (Оранжевий пунктир)
    ax.plot(timestamps, arima_pred, color='orange', linestyle='--', linewidth=1.5, label=f'Прогноз ARIMA (RMSE={rmse_arima:.2f})')
    
    # 3. Прогноз LSTM (Синя суцільна лінія)
    ax.plot(timestamps, lstm_pred, color='blue', linestyle='-', linewidth=1.5, label=f'Прогноз LSTM (RMSE={rmse_lstm:.2f})')

    # Оформлення
    ax.set_title(f'Порівняння прогнозів: LSTM vs ARIMA ({version}) (Фрагмент 1 тиждень)', color='black')
    ax.set_xlabel('Часові кроки (Години)', color='black')
    ax.set_ylabel('Навантаження (МВт)', color='black')
    ax.tick_params(colors='black')
    ax.grid(True, linestyle='-', alpha=0.3, color='gray')
    ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='lightgray')

    plt.tight_layout()
    plt.savefig(f"forecast_comparison_{version}_test.png", dpi=300, bbox_inches='tight')
    plt.close()

# --- Тестові дані ---
if __name__ == "__main__":
    e_lstm = np.random.normal(0, 100, 1000)
    e_arima = np.random.normal(50, 150, 1000)
    plot_error_distribution(e_lstm, e_arima, 0, 100, 50, 150)
    
    steps = np.arange(168)
    actual = 500 + 100 * np.sin(2 * np.pi * steps / 24) + np.random.normal(0, 20, 168)
    l_pred = 500 + 95 * np.sin(2 * np.pi * steps / 24)
    a_pred = 510 + 90 * np.sin(2 * np.pi * (steps-2) / 24)
    plot_forecast_comparison(steps, actual, l_pred, a_pred, 15.2, 25.4)
    print("✅ Графіки успішно згенеровані!")
