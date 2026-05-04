# ATLAS_PASSPORT: docs/system/map/ml_core_engine.md
import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_forecast(actual, predicted, title="Forecast", save_path=None):
    plt.figure(figsize=(12, 6))
    plt.plot(actual, label='Actual')
    plt.plot(predicted, label='Predicted')
    plt.title(title)
    plt.legend()
    if save_path:
        plt.savefig(save_path)
    plt.close()
