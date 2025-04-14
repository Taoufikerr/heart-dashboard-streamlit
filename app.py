
import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données
df = pd.read_csv("heart.csv")

st.set_page_config(page_title="Dashboard Cardiaque Enrichi", layout="wide")
st.title("💡 Dashboard Cardiaque Intelligent - Analyse Interactive")

# Filtres
st.sidebar.header("🎛️ Filtres")

sex_filter = st.sidebar.selectbox("Sexe", ["Tous", "Homme", "Femme"])
target_filter = st.sidebar.selectbox("Maladie Cardiaque", ["Tous", "Malade", "Pas de maladie"])
age_min, age_max = int(df["age"].min()), int(df["age"].max())
age_range = st.sidebar.slider("Âge", min_value=age_min, max_value=age_max, value=(age_min, age_max))

cp_options = ["Tous"] + sorted(df["cp"].astype(str).unique().tolist())
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

# 📌 Interprétation dynamique
st.markdown("### 🧠 Interprétation automatique")

if filtered_df['target'].mean() > 0.6:
    st.info("🔍 Forte proportion de patients malades dans les filtres appliqués.")
elif filtered_df['target'].mean() < 0.3:
    st.success("✅ Faible proportion de patients malades dans cet échantillon.")
else:
    st.warning("ℹ️ Proportion modérée de patients malades.")

if filtered_df["age"].mean() > 55:
    st.markdown("📌 L’âge moyen élevé peut indiquer un risque accru.")

# 📊 Graphiques avec descriptions
st.subheader("📊 Graphiques Interactifs")

st.plotly_chart(
    px.pie(filtered_df, names=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
           title="Répartition des cas de Maladie Cardiaque"),
    use_container_width=True
)
st.caption("👉 Ce graphique montre la proportion de patients malades selon les filtres sélectionnés.")

st.plotly_chart(
    px.histogram(filtered_df, x="age", color=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
                 nbins=20, title="Distribution de l'âge par statut de maladie"),
    use_container_width=True
)
st.caption("👉 Ce graphique montre la distribution des âges pour chaque groupe (malade ou non).")

st.plotly_chart(
    px.scatter(filtered_df, x="age", y="chol", color=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}),
               title="Âge vs Cholestérol"),
    use_container_width=True
)
st.caption("👉 Ce graphique permet de repérer visuellement une corrélation entre l’âge et le cholestérol.")

st.plotly_chart(
    px.box(filtered_df, x="target", y="thalach", title="Fréquence Cardiaque Max selon Maladie",
           labels={"target": "Maladie", "thalach": "Fréquence Cardiaque Max"}),
    use_container_width=True
)
st.caption("👉 Ce boxplot compare la fréquence cardiaque max chez les patients malades vs non malades.")

# 📋 Données + export
st.subheader("📄 Données filtrées")
st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Télécharger les données filtrées", data=csv, file_name="donnees_filtrees.csv", mime="text/csv")
