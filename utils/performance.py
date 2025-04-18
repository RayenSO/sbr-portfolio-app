import pandas as pd
import numpy as np
from scipy.stats import linregress

def monthly_returns(series):
    """Convertit une série de valeurs (VL) en rendements mensuels."""
    return series.resample('M').last().pct_change().dropna()

def max_drawdown(series):
    """Calcule le max drawdown d'une série de valeurs."""
    cum_max = series.cummax()
    drawdown = (series - cum_max) / cum_max
    return drawdown.min()

def performance_metrics(portfolio_vl, benchmark_prices, rf_rate=0.03):
    """Calcule les métriques de performance mensuelle pour un mois donné."""

    # Rendements quotidiens
    port_daily_returns = portfolio_vl.pct_change().dropna()
    bmk_daily_returns = benchmark_prices.pct_change().dropna()
    
    # Alignement des dates
    aligned = pd.concat([port_daily_returns, bmk_daily_returns], axis=1, join="inner")
    aligned.columns = ['port', 'bmk']

    if len(aligned) < 2:
        return {}

    port = aligned['port']
    bmk = aligned['bmk']

    # Risk-free rate daily (approximatif)
    rf_daily = (1 + rf_rate) ** (1/252) - 1
    excess_returns = port - rf_daily

    # --- Calculs ---
    perf = (portfolio_vl[-1] / portfolio_vl[0]) - 1
    perf_bmk = (benchmark_prices[-1] / benchmark_prices[0]) - 1
    vol = port.std() * np.sqrt(252)
    vol_bmk = bmk.std() * np.sqrt(252)
    sharpe = excess_returns.mean() / port.std() * np.sqrt(252)
    sortino = excess_returns.mean() / port[port < 0].std() * np.sqrt(252)
    beta, alpha, r_value, _, _ = linregress(bmk, port)
    correlation = port.corr(bmk)
    r2 = r_value ** 2
    treynor = excess_returns.mean() * 252 / beta if beta != 0 else np.nan
    tracking_error = np.std(port - bmk) * np.sqrt(252)
    info_ratio = (port.mean() - bmk.mean()) / tracking_error if tracking_error != 0 else np.nan
    mdd_port = max_drawdown(portfolio_vl)
    mdd_bmk = max_drawdown(benchmark_prices)

    return {
        "Performance": (perf, perf_bmk),
        "Volatilité": (vol, vol_bmk),
        "Sharpe": (sharpe, None),
        "Sortino": (sortino, None),
        "Beta": (beta, None),
        "Corrélation": (correlation, None),
        "R²": (r2, None),
        "Treynor": (treynor, None),
        "Information Ratio": (info_ratio, None),
        "Tracking Error": (tracking_error, None),
        "Max Drawdown": (mdd_port, mdd_bmk)
    }
