
import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv("heart.csv")

st.set_page_config(page_title="Dashboard Cardiaque", layout="wide")

st.title("📊 Dashboard Interactif - Données Cardiaques")

# Sidebar filters
st.sidebar.header("Filtres")

# Filtrer par sexe
sex_filter = st.sidebar.selectbox("Sexe", options=["Tous", "Homme", "Femme"])

# Filtrer par présence de maladie
target_filter = st.sidebar.selectbox("Maladie Cardiaque", options=["Tous", "Malade", "Pas de maladie"])

# Slider pour l'âge
age_min, age_max = int(df["age"].min()), int(df["age"].max())
age_range = st.sidebar.slider("Âge", min_value=age_min, max_value=age_max, value=(age_min, age_max))

# Application des filtres
filtered_df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]

if sex_filter != "Tous":
    filtered_df = filtered_df[filtered_df["sex"] == (1 if sex_filter == "Homme" else 0)]

if target_filter != "Tous":
    filtered_df = filtered_df[filtered_df["target"] == (1 if target_filter == "Malade" else 0)]

# Pie Chart
st.plotly_chart(
    px.pie(filtered_df, names=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
           title="Répartition des cas de Maladie Cardiaque")
)

# Scatter plot
st.plotly_chart(
    px.scatter(filtered_df, x="age", y="chol", color=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
               title="Âge vs Cholestérol", labels={"chol": "Cholestérol", "age": "Âge"})
)

# Histogramme
st.plotly_chart(
    px.histogram(filtered_df, x="age", color=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
                 nbins=20, title="Distribution de l'âge")
)

# Box plot
st.plotly_chart(
    px.box(filtered_df, x="target", y="thalach", title="Fréquence Cardiaque Max selon Maladie",
           labels={"target": "Maladie", "thalach": "Fréquence Cardiaque Max"})
)
