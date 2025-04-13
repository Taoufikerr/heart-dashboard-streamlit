
import streamlit as st
import pandas as pd
import plotly.express as px

# Chargement des données
df = pd.read_csv("heart.csv")

st.set_page_config(page_title="Dashboard Cardiaque Complet", layout="wide")
st.title("💓 Tableau de Bord Cardiaque - Analyse Complète")

# Sidebar - Filtres
st.sidebar.header("🎛️ Filtres")

# Sexe
sex_filter = st.sidebar.selectbox("Sexe", ["Tous", "Homme", "Femme"])

# Maladie
target_filter = st.sidebar.selectbox("Maladie Cardiaque", ["Tous", "Malade", "Pas de maladie"])

# Tranche d'âge
age_min, age_max = int(df["age"].min()), int(df["age"].max())
age_range = st.sidebar.slider("Âge", min_value=age_min, max_value=age_max, value=(age_min, age_max))

# Type de douleur thoracique (cp)
cp_options = ["Tous"] + sorted(df["cp"].unique().astype(str).tolist())
cp_filter = st.sidebar.selectbox("Type de douleur thoracique (cp)", cp_options)

# Application des filtres
filtered_df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]

if sex_filter != "Tous":
    filtered_df = filtered_df[filtered_df["sex"] == (1 if sex_filter == "Homme" else 0)]

if target_filter != "Tous":
    filtered_df = filtered_df[filtered_df["target"] == (1 if target_filter == "Malade" else 0)]

if cp_filter != "Tous":
    filtered_df = filtered_df[filtered_df["cp"] == int(cp_filter)]

# METRICS
col1, col2, col3 = st.columns(3)
col1.metric("Âge moyen", f"{filtered_df['age'].mean():.1f} ans")
col2.metric("Cholestérol moyen", f"{filtered_df['chol'].mean():.1f} mg/dL")
col3.metric("Patients malades (%)", f"{filtered_df['target'].mean() * 100:.1f} %")

# GRAPHIQUES
st.subheader("📊 Visualisations interactives")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        px.pie(filtered_df, names=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
               title="Répartition des cas de Maladie Cardiaque"), use_container_width=True
    )

with col2:
    st.plotly_chart(
        px.histogram(filtered_df, x="age", color=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
                     nbins=20, title="Distribution de l'âge"), use_container_width=True
    )

st.plotly_chart(
    px.scatter(filtered_df, x="age", y="chol", color=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
               title="Âge vs Cholestérol", labels={"chol": "Cholestérol", "age": "Âge"}), use_container_width=True
)

st.plotly_chart(
    px.box(filtered_df, x="target", y="thalach", title="Fréquence Cardiaque Max selon Maladie",
           labels={"target": "Maladie", "thalach": "Fréquence Cardiaque Max"}), use_container_width=True
)

# DONNÉES FILTRÉES
st.subheader("📋 Données filtrées")

st.dataframe(filtered_df)

# TÉLÉCHARGEMENT
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Télécharger les données filtrées en CSV", data=csv, file_name="filtered_heart_data.csv", mime="text/csv")

