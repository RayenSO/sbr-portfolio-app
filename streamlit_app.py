import streamlit as st
import pandas as pd

from data.loader import load_all_data
from vues.vl_quotidienne import afficher_page_vl
from vues.positions_mensuelles import afficher_positions_mensuelles
from vues.performance_globale import afficher_performance_globale

# Chargement des données
ordres, prix_titres, jours_marche, benchmark = load_all_data()

# Chargement des fichiers calculés (générés ailleurs)
positions = pd.read_csv("data/positions_quotidiennes.csv", index_col=0, parse_dates=True)
cash = pd.read_csv("data/cash_quotidien.csv", index_col=0, parse_dates=True)
vl = pd.read_csv("data/vl_quotidienne.csv", index_col=0, parse_dates=True)
vl.columns = ["VL Totale"] 
# Choix de la page
page = st.sidebar.selectbox("Page", ["📊 VL quotidienne", "📅 Positions mensuelles", "📈 Performance Globale"])

if page == "📊 VL quotidienne":
    afficher_page_vl(prix_titres, positions, cash, benchmark)

elif page == "📅 Positions mensuelles":

    afficher_positions_mensuelles(jours_marche, prix_titres, positions, cash, vl, benchmark)

elif page == "📈 Performance Globale":
    afficher_performance_globale(vl, benchmark)
