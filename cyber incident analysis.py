import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
import ipywidgets as widgets
from IPython.display import display



df = pd.read_csv("cyber_incidents.csv", parse_dates=["date"])


df["year"] = df["date"].dt.year


years = sorted(df["year"].unique())
attack_types = sorted(df["attack_type"].unique())

year_dropdown = widgets.Dropdown(options=["Усі"] + years, description="Рік:")
attack_dropdown = widgets.Dropdown(options=["Усі"] + attack_types, description="Тип атаки:")

def update_stats(year, attack_type):
    
    filtered = df.copy()
    if year != "Усі":
        filtered = filtered[filtered["year"] == year]
    if attack_type != "Усі":
        filtered = filtered[filtered["attack_type"] == attack_type]

    
    sector_stats = filtered["sector"].value_counts()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=sector_stats.values, y=sector_stats.index)
    plt.title("Кількість атак за секторами")
    plt.xlabel("Кількість інцидентів")
    plt.ylabel("Сектор")
    plt.show()

    
    
    if len(filtered) >= 3:
        X = filtered[["losses", "year"]].dropna()
        kmeans = KMeans(n_clusters=3, random_state=42)
        filtered["cluster"] = kmeans.fit_predict(X)

        plt.figure(figsize=(6, 5))
        plt.scatter(filtered["year"], filtered["losses"], c=filtered["cluster"], cmap="viridis")
        plt.title("Кластеризація кіберінцидентів (K-Means)")
        plt.xlabel("Рік")
        plt.ylabel("Втрати, $")
        plt.show()
    else:
        print("Недостатньо даних для кластеризації.")


widgets.interactive(update_stats, year=year_dropdown, attack_type=attack_dropdown)
