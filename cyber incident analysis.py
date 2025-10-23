import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import random
import os

st.set_page_config(page_title="Аналіз кіберінцидентів", layout="wide")
st.title("🛡️ Аналіз кіберінцидентів")

filename = "cyber_incidents.csv"

if not os.path.exists(filename):
    st.warning("Файл cyber_incidents.csv не знайдено — створюємо тестові дані...")
    attack_types = ["Phishing", "Ransomware", "DDoS", "Malware", "Insider Attack", "SQL Injection"]
    sectors = ["Finance", "Healthcare", "Education", "Government", "Energy", "Retail", "IT"]
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2025, 10, 1)

    def random_date(start, end):
        return start + timedelta(days=random.randint(0, (end - start).days))

    data = []
    for _ in range(20):
        date = random_date(start_date, end_date).strftime("%Y-%m-%d")
        attack = random.choice(attack_types)
        sector = random.choice(sectors)
        losses = random.randint(1000, 500000)
        data.append([date, attack, sector, losses])

    df = pd.DataFrame(data, columns=["date", "attack_type", "sector", "losses"])
    df.to_csv(filename, index=False)
    st.success(f"✅ Створено файл '{filename}' з тестовими даними.")
else:
    df = pd.read_csv(filename, parse_dates=["date"])

df["year"] = df["date"].dt.year

col1, col2 = st.columns(2)
years = ["Усі"] + sorted(df["year"].unique().tolist())
attack_types = ["Усі"] + sorted(df["attack_type"].unique().tolist())

year = col1.selectbox("Виберіть рік:", years)
attack = col2.selectbox("Виберіть тип атаки:", attack_types)

filtered = df.copy()
if year != "Усі":
    filtered = filtered[filtered["year"] == year]
if attack != "Усі":
    filtered = filtered[filtered["attack_type"] == attack]

st.write(f"📊 Відображено {len(filtered)} записів після фільтрації.")

st.subheader("📈 Кількість атак за секторами")

sector_stats = filtered["sector"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=sector_stats.values, y=sector_stats.index, ax=ax)
ax.set_xlabel("Кількість інцидентів")
ax.set_ylabel("Сектор")
st.pyplot(fig)

st.subheader("🤖 Кластеризація кіберінцидентів (K-Means)")

if len(filtered) >= 3:
    X = filtered[["losses", "year"]].dropna()
    kmeans = KMeans(n_clusters=3, random_state=42)
    filtered["cluster"] = kmeans.fit_predict(X)

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    scatter = ax2.scatter(filtered["year"], filtered["losses"], c=filtered["cluster"], cmap="viridis")
    ax2.set_xlabel("Рік")
    ax2.set_ylabel("Втрати ($)")
    ax2.set_title("Результати кластеризації")
    st.pyplot(fig2)
else:
    st.info("Недостатньо даних для кластеризації.")

st.subheader("🗂️ Дані інцидентів")
st.dataframe(filtered)


