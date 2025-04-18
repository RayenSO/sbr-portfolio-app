import streamlit as st
import pandas as pd
from utils.performance import performance_metrics
import plotly.express as px

def afficher_positions_mensuelles(jours_marche, prix_titres, positions, cash, vl, benchmark, ordres):
    st.header("📅 Positions à la fin d’un mois sélectionné")

    prix_titres = prix_titres.set_index("Date").apply(pd.to_numeric, errors='coerce')
    mois_fin = jours_marche.groupby([jours_marche.dt.year, jours_marche.dt.month]).max()
    mois_disponibles = pd.to_datetime(mois_fin.values)

    options = [d.strftime("%B %Y") for d in mois_disponibles]
    choix = st.selectbox("Choisir un mois", options, index=len(options) - 1)
    date_selection = mois_disponibles[options.index(choix)]

    # Affichage des positions
    st.subheader(f"📆 Données pour : {date_selection.strftime('%d %B %Y')}")
    pos = positions.loc[date_selection]
    prix_jour = prix_titres.loc[date_selection]
    val = pos * prix_jour
    val = val[val > 0]

    df = pd.DataFrame({
        "Nb actions": pos[val.index],
        "Prix": prix_jour[val.index],
        "Valeur": val
    })

    st.dataframe(df.style.format({"Prix": "{:.2f}", "Valeur": "{:.2f}", "Nb actions": "{:.0f}"}))

    montant_cash = float(cash.loc[date_selection])
    st.markdown(f"💼 **Titres** : {val.sum():,.2f} $")
    st.markdown(f"💵 **Cash** : {montant_cash:,.2f} $")
    st.markdown(f"📈 **Total portefeuille** : {val.sum() + montant_cash:,.2f} $")

    # === Bloc performance mensuelle ===
    st.subheader("📊 Indicateurs mensuels : Portefeuille vs Benchmark")

    # Déterminer la plage du mois sélectionné
    year, month = date_selection.year, date_selection.month
    date_debut = pd.Timestamp(year=year, month=month, day=1)
    date_fin = date_selection
    

    # Extraire les données du mois
    col_vl = vl.columns[0]  # safe car il n'y a qu'une seule colonne
    vl_mois = vl.loc[date_debut:date_fin, col_vl]
    benchmark_mois = benchmark.loc[(benchmark.index >= date_debut) & (benchmark.index <= date_fin), "Prix"]

    if len(vl_mois) > 1 and len(benchmark_mois) > 1:
        metrics = performance_metrics(vl_mois, benchmark_mois)
        df_perf = pd.DataFrame(metrics, index=["Portefeuille", "Benchmark"]).T

        # Format spécifique par indicateur
        def format_cell(row_name, value, col_name):
            if pd.isna(value):
                return "-"
            if row_name in ["Performance", "Volatilité", "Tracking Error", "Max Drawdown"]:
                return f"{value:.2%}"
            elif col_name == "Benchmark":
                return "-"
            else:
                return f"{value:.2f}"

        # Application du format à chaque cellule
        for row in df_perf.index:
            for col in df_perf.columns:
                df_perf.loc[row, col] = format_cell(row, df_perf.loc[row, col], col)

        st.dataframe(df_perf)
        # === Bloc répartition sectorielle (camembert) ===
        st.subheader("🥧 Répartition sectorielle (GICS Class)")

        # Préparer les données GICS Class depuis la feuille Ordres
        gics_map = ordres[["Ticker", "GICS Class"]].dropna().drop_duplicates(subset="Ticker", keep="last").set_index("Ticker")

        # Positions du jour
        positions_du_mois = pos[val.index]  # uniquement les titres détenus
        prix_du_jour = prix_jour[val.index]

        # Valorisation par titre
        df_repartition = pd.DataFrame({
            "Nb actions": positions_du_mois,
            "Prix": prix_du_jour,
        })
        df_repartition["Valeur"] = df_repartition["Nb actions"] * df_repartition["Prix"]

        # Ajouter GICS Class
        df_repartition["GICS Class"] = df_repartition.index.map(gics_map["GICS Class"])

        # Grouper par secteur
        df_secteurs = df_repartition.groupby("GICS Class")["Valeur"].sum().sort_values(ascending=False)

        # Affichage
        st.dataframe(df_secteurs.to_frame("Valeur ($)").style.format("{:.2f}"))

        # Affichage camembert
        fig = px.pie(
            df_secteurs.reset_index(),
            values="Valeur",
            names="GICS Class",
            title="Répartition sectorielle du portefeuille",
            hole=0.3  
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Données insuffisantes pour calculer les métriques de performance.")
