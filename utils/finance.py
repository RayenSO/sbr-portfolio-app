import pandas as pd

def calcul_vl(positions, cash, prix_titres):
    prix_titres.index = pd.to_datetime(prix_titres.index)
    prix_titres = prix_titres.apply(pd.to_numeric, errors='coerce')
    vl_titres = (positions * prix_titres).sum(axis=1)
    vl_cash = cash.squeeze()
    vl_total = vl_titres + vl_cash
    df = pd.DataFrame({
        "Cash ($)": vl_cash,
        "Titres ($)": vl_titres,
        "VL Totale ($)": vl_total
    })
    return df.dropna()

def normaliser_series(s):
    return 100 * s / s.iloc[0]
