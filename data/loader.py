import pandas as pd

def load_all_data(file_path="data.xlsx"):
    xls = pd.ExcelFile(file_path)
    ordres = pd.read_excel(xls, "Ordres")
    prix_titres = pd.read_excel(xls, "Prix_Titres")
    jours_marche = pd.read_excel(xls, "Jour_Marche")
    benchmark = pd.read_excel(xls, "Benchmark")
    
    # Nettoyages communs
    jours_marche = pd.to_datetime(jours_marche["Date"], dayfirst=True).sort_values()
    benchmark["Date"] = pd.to_datetime(benchmark["Date"], dayfirst=True)
    benchmark.set_index("Date", inplace=True)
    prix_titres["Date"] = pd.to_datetime(prix_titres["Date"], dayfirst=True)
    
    return ordres, prix_titres, jours_marche, benchmark
