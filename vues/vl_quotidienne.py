import streamlit as st
import pandas as pd
from utils.finance import calcul_vl, normaliser_series

def afficher_page_vl(prix_titres, positions, cash, benchmark):
    st.header("📊 VL quotidienne : Cash + Titres + Benchmark")

    prix_titres = prix_titres.set_index("Date").apply(pd.to_numeric, errors='coerce')
    vl_df = calcul_vl(positions, cash, prix_titres)

    st.subheader("📋 Décomposition journalière de la VL")
    st.dataframe(vl_df.style.format("{:.2f}"))

    # Benchmark normalisé
    benchmark = benchmark.loc[vl_df.index]
    prix_bmk_norm = normaliser_series(benchmark["Prix"])
    vl_norm = normaliser_series(vl_df["VL Totale ($)"])

    df_plot = pd.DataFrame({
        "VL Totale (norm.)": vl_norm,
        "Benchmark (norm.)": prix_bmk_norm
    })

    st.subheader("📈 VL vs Benchmark")
    st.line_chart(df_plot)
