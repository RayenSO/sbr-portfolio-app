import streamlit as st
import pandas as pd
from utils.performance import performance_metrics

def afficher_performance_globale(vl, benchmark):
    st.header("📈 Performance Globale")

    # Définir les périodes
    date_inception = pd.Timestamp("2024-01-16")
    date_end = vl.index.max()
    date_ytd = pd.Timestamp("2025-01-01")

    # Extraire les données
    vl_incep = vl.loc[date_inception:date_end].squeeze()
    bmk_incep = benchmark.loc[date_inception:date_end, "Prix"]

    vl_ytd = vl.loc[date_ytd:date_end].squeeze()
    bmk_ytd = benchmark.loc[date_ytd:date_end, "Prix"]

    # Inception
    st.subheader("🔁 Depuis le 16 janvier 2024")
    if len(vl_incep) > 1 and len(bmk_incep) > 1:
        metrics_incep = performance_metrics(vl_incep, bmk_incep)
        df_incep = pd.DataFrame(metrics_incep, index=["Portefeuille", "Benchmark"]).T
        df_incep = apply_custom_formatting(df_incep)
        st.dataframe(df_incep)
    else:
        st.warning("Données insuffisantes pour la période d'inception.")

    # YTD
    st.subheader("📅 Year-To-Date (YTD 2025)")
    if len(vl_ytd) > 1 and len(bmk_ytd) > 1:
        metrics_ytd = performance_metrics(vl_ytd, bmk_ytd)
        df_ytd = pd.DataFrame(metrics_ytd, index=["Portefeuille", "Benchmark"]).T
        df_ytd = apply_custom_formatting(df_ytd)
        st.dataframe(df_ytd)
    else:
        st.warning("Données insuffisantes pour le YTD.")
    

def apply_custom_formatting(df):
    percent_metrics = ["Performance", "Volatilité", "Tracking Error", "Max Drawdown"]
    decimal_metrics = ["Sharpe", "Sortino", "Beta", "Corrélation", "R²", "Treynor", "Information Ratio"]

    for metric in df.index:
        for col in df.columns:
            val = df.loc[metric, col]
            if pd.isna(val):
                df.loc[metric, col] = "-"
            elif metric in percent_metrics:
                df.loc[metric, col] = f"{val:.2%}"
            elif metric in decimal_metrics:
                df.loc[metric, col] = "-" if col == "Benchmark" else f"{val:.2f}"
            else:
                df.loc[metric, col] = f"{val:.2f}"
    return df
