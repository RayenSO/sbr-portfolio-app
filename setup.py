# setup.py
import pandas as pd
import numpy as np
from datetime import datetime

# === Paramètres
capital_initial = 100000
taux_cash_quotidien = (1 + 0.03) ** (1 / 252) - 1

# === Chargement des données Excel
xls = pd.ExcelFile("data.xlsx")
ordres = pd.read_excel(xls, "Ordres")
prix = pd.read_excel(xls, "Prix_Titres")
jours_marche = pd.read_excel(xls, "Jour_Marche")

# Nettoyage
ordres['Date'] = pd.to_datetime(ordres['Date'], dayfirst=True)
prix['Date'] = pd.to_datetime(prix['Date'], dayfirst=True)
prix.set_index('Date', inplace=True)
prix = prix.apply(pd.to_numeric, errors='coerce')
jours_marche = pd.to_datetime(jours_marche["Date"], dayfirst=True)

# Liste des dates à traiter
dates = jours_marche
tickers = prix.columns.tolist()

# === Initialisation des structures
positions_df = pd.DataFrame(index=dates, columns=tickers).fillna(0)
cash_series = pd.Series(index=dates, dtype=float)
vl_series = pd.Series(index=dates, dtype=float)

positions = {ticker: 0 for ticker in tickers}
current_cash = capital_initial

# === Boucle principale
for i, date in enumerate(dates):
    if i > 0:
        current_cash *= (1 + taux_cash_quotidien)

    # Ordres du jour
    day_orders = ordres[ordres["Date"] == date]
    for _, order in day_orders.iterrows():
        ticker = order["Ticker"]
        n = order["Nb actions"]
        prix_unit = order["Prix local unitaire"]
        frais = order["Frais"]
        type_ord = order["Type"].lower()

        montant = n * prix_unit
        if type_ord == "achat":
            current_cash -= montant + frais
            positions[ticker] += n
        elif type_ord == "vente":
            current_cash += montant - frais
            positions[ticker] -= n
        elif type_ord == "short":
            current_cash += montant - frais
            positions[ticker] -= n
        elif type_ord == "rachat":
            current_cash -= montant + frais
            positions[ticker] += n

    # Enregistrement
    for ticker in tickers:
        positions_df.loc[date, ticker] = positions[ticker]
    cash_series.loc[date] = current_cash

    # VL = cash + valeur titres
    if date in prix.index:
        prix_jour = prix.loc[date]
        val_titres = sum(positions[t] * prix_jour[t] for t in tickers if t in prix_jour)
        vl_series.loc[date] = current_cash + val_titres
    else:
        vl_series.loc[date] = np.nan

# === Sauvegarde des résultats
positions_df.to_csv("data/positions_quotidiennes.csv")
cash_series.to_csv("data/cash_quotidien.csv")
vl_series.to_csv("data/vl_quotidienne.csv")

print("✅ Données calculées et sauvegardées.")
