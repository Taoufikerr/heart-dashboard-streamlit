
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Charger les données avec date
df = pd.read_csv("heart.csv")
df["date_exam"] = pd.to_datetime(df["date_exam"])

st.set_page_config(page_title="Dashboard Cardiaque Final", layout="wide")
st.title("🧠 Dashboard Cardiaque Avancé avec Analyse Temporelle & Recommandations")

# 🎛️ Filtres
st.sidebar.header("Filtres")
sex_filter = st.sidebar.selectbox("Sexe", ["Tous", "Homme", "Femme"])
target_filter = st.sidebar.selectbox("Maladie Cardiaque", ["Tous", "Malade", "Pas de maladie"])
cp_filter = st.sidebar.selectbox("Type de douleur (cp)", ["Tous"] + sorted(df["cp"].astype(str).unique().tolist()))
date_range = st.sidebar.date_input("Période d'examen", [df["date_exam"].min(), df["date_exam"].max()])

# Application des filtres
filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df["date_exam"] >= pd.to_datetime(date_range[0])) & (filtered_df["date_exam"] <= pd.to_datetime(date_range[1]))]

if sex_filter != "Tous":
    filtered_df = filtered_df[filtered_df["sex"] == (1 if sex_filter == "Homme" else 0)]
if target_filter != "Tous":
    filtered_df = filtered_df[filtered_df["target"] == (1 if target_filter == "Malade" else 0)]
if cp_filter != "Tous":
    filtered_df = filtered_df[filtered_df["cp"] == int(cp_filter)]

# 📊 KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Âge moyen", f"{filtered_df['age'].mean():.1f} ans")
col2.metric("Cholestérol moyen", f"{filtered_df['chol'].mean():.1f} mg/dL")
col3.metric("Patients malades (%)", f"{filtered_df['target'].mean() * 100:.1f} %")

# 💬 Commentaires dynamiques
st.markdown("### 🤖 Interprétation intelligente")
if filtered_df.empty:
    st.warning("Aucune donnée ne correspond à ces filtres.")
else:
    age_avg = filtered_df["age"].mean()
    target_pct = filtered_df["target"].mean() * 100
    cp_common = filtered_df["cp"].mode()[0] if not filtered_df["cp"].mode().empty else "N/A"

    if target_pct > 60:
        st.info("🔴 Forte proportion de patients malades dans les filtres appliqués.")
    elif target_pct < 30:
        st.success("🟢 Faible proportion de patients malades dans cet échantillon.")
    else:
        st.warning("🟡 Proportion modérée de patients malades.")

    if age_avg > 55:
        st.markdown("📌 L'âge moyen est élevé, ce qui peut refléter un risque cardiovasculaire accru.")
    if sex_filter == "Femme" and age_avg > 60:
        st.markdown("👩‍⚕️ Chez les femmes âgées de plus de 60 ans, une attention particulière est recommandée.")
    st.markdown(f"📈 Type de douleur le plus fréquent dans l'échantillon : **cp = {cp_common}**")

# 📄 Résumé rapport
with st.expander("📄 Rapport synthétique (à copier/coller si besoin)"):
    st.text_area("Résumé automatique :", 
    f"""Analyse réalisée sur {len(filtered_df)} patients.
Période sélectionnée : du {date_range[0]} au {date_range[1]}.
Âge moyen : {age_avg:.1f} ans.
Proportion de malades : {target_pct:.1f} %.
Type de douleur dominant : cp = {cp_common}.
""", height=180)

# 📈 Visualisation temporelle
st.markdown("### 📅 Évolution temporelle")
fig_time = px.histogram(filtered_df, x="date_exam", color=filtered_df["target"].map({0:"Pas de Maladie", 1:"Malade"}), nbins=30, title="Cas par date d'examen")
st.plotly_chart(fig_time, use_container_width=True)
st.caption("👉 Histogramme des cas en fonction de la date des examens.")

# 📊 Graphiques classiques
st.markdown("### 📊 Visualisations par variable")
st.plotly_chart(px.pie(filtered_df, names=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}), title="Répartition Maladie"), use_container_width=True)
st.plotly_chart(px.scatter(filtered_df, x="age", y="chol", color=filtered_df["target"].map({0: "Pas de Maladie", 1: "Malade"}), title="Âge vs Cholestérol"), use_container_width=True)
st.plotly_chart(px.box(filtered_df, x="target", y="thalach", title="Fréquence Cardiaque Max selon Maladie", labels={"target": "Maladie", "thalach": "Fréquence Cardiaque Max"}), use_container_width=True)

# 📋 Tableau & export
st.markdown("### 📋 Données filtrées")
st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Télécharger les données filtrées", data=csv, file_name="donnees_filtrees.csv", mime="text/csv")
