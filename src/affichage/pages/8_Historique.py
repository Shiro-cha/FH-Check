# src/affichage/pages/8_Historique.py
import streamlit as st
import pandas as pd
page = st.sidebar.radio("Navigation", ["Affichage dataset", "Apprentissage", "Démonstration", "Bilan", "Autres pages", "Historique"])
st.markdown("""
<style>
/* --- Sidebar --- */
[data-testid="stSidebar"] {
    background: #f7f7f7;
    border-right: 1px solid #e0e0e0;
    padding-top: 10px;
}
/* Masquer complètement la barre supérieure (3 points + Deploy) */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
[data-testid="stSidebar"]::before {
    content: "📡";
    display: block;
    font-size: 75px;
    text-align: center;
    margin-bottom: 10px;
    color: #6a0dad;
}

/* Liens sidebar */
[data-testid="stSidebarNav"] ul li a {
    border-radius: 8px;
    margin: 4px 8px;
    padding: 8px 12px;
    font-weight: 600;
    color: #333 !important;
    transition: 0.3s;
}
[data-testid="stSidebarNav"] ul li a:hover {
    background: #e7def9 !important;
    color: #000 !important;
}

/* --- Fond général --- */
.stApp, .main, .block-container {
    background: #f9f9f9 !important;
    padding: 15px 20px;
}


/* --- FH-Check Card (grand titre) --- */
.title-card {
    background: #f4edf9;
    padding: 40px 50px;                 /* plus de padding */
    border-radius: 20px;
    text-align: center;
    font-size: 42px;               /* taille augmentée */
    font-weight: 800;
    color: #6a0dad;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08); /* ombre plus marquée */
    margin-bottom: 30px;
}
.title-sub {
    font-size: 18px;               /* un peu plus grand */
    font-weight: 500;
    margin-top: 10px;
    color: #444;
}


</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Historique FH", layout="wide")
st.title("Historique des Démonstrations FH")

# -------------------------------
# Initialisation historique
# -------------------------------
if "historique_sessions" not in st.session_state:
    st.session_state["historique_sessions"] = []

# Récupération de la session courante depuis démonstration/bilan
if "df_test" in st.session_state and "historique_etat" in st.session_state:
    if st.button("Sauvegarder cette démonstration dans l'historique"):
        new_entry = {
            "data": st.session_state["df_test"].copy(),
            "etat": st.session_state["historique_etat"].copy(),
            "file": st.session_state.get("uploaded_file_name", "session"),
        }
        st.session_state["historique_sessions"].append(new_entry)
        st.success("Session sauvegardée avec succès")

# -------------------------------
# Affichage historique
# -------------------------------
if len(st.session_state["historique_sessions"]) == 0:
    st.info("Aucune session enregistrée. Lancez une démonstration pour remplir l’historique.")
    st.stop()

st.subheader("Résumé des Sessions")
summary_rows = []

for idx, entry in enumerate(st.session_state["historique_sessions"]):
    etats = entry["etat"]
    nb_total = len(etats)
    nb_ok = etats.count("OK")
    nb_deg = etats.count("Dégradée")
    nb_ko = etats.count("KO")
    quality = (nb_ok*1.0 + nb_deg*0.5) / nb_total * 100
    summary_rows.append({
        "Session": idx+1,
        "Fichier": entry.get("file", f"session_{idx+1}"),
        "Durée (s)": nb_total,
        "%OK": f"{nb_ok/nb_total*100:.1f}",
        "%Dégradée": f"{nb_deg/nb_total*100:.1f}",
        "%KO": f"{nb_ko/nb_total*100:.1f}",
        "Qualité Globale": f"{quality:.1f}"
    })

df_summary = pd.DataFrame(summary_rows)
st.dataframe(df_summary, use_container_width=True)

# -------------------------------
# Sélection d'une session
# -------------------------------
st.subheader("Détails d’une Session")
session_choice = st.selectbox(
    "Choisir une session à analyser :",
    options=list(range(1, len(st.session_state["historique_sessions"])+1)),
    format_func=lambda x: f"Session {x}"
)

entry = st.session_state["historique_sessions"][session_choice-1]
historique_etat = entry["etat"]

# -------------------------------
# Statistiques (à la place du graphique)
# -------------------------------
st.markdown("### Statistiques de la session sélectionnée")

nb_total = len(historique_etat)
nb_ok = historique_etat.count("OK")
nb_deg = historique_etat.count("Dégradée")
nb_ko = historique_etat.count("KO")

col1, col2, col3 = st.columns(3)
col1.metric("OK", f"{nb_ok} ({nb_ok/nb_total*100:.1f}%)")
col2.metric("Dégradée", f"{nb_deg} ({nb_deg/nb_total*100:.1f}%)")
col3.metric("KO", f"{nb_ko} ({nb_ko/nb_total*100:.1f}%)")

# Tableau détaillé
st.markdown("### Tableau récapitulatif")
stats_df = pd.DataFrame({
    "État": ["OK", "Dégradée", "KO"],
    "Durée (s)": [nb_ok, nb_deg, nb_ko],
    "Pourcentage (%)": [f"{nb_ok/nb_total*100:.1f}", f"{nb_deg/nb_total*100:.1f}", f"{nb_ko/nb_total*100:.1f}"]
})
st.table(stats_df)

# -------------------------------
# Reset bouton
# -------------------------------
st.markdown("---")
if st.button("Vider l’historique complet"):
    st.session_state["historique_sessions"] = []
    st.warning("Historique effacé.")
if st.button("Next"):
    st.switch_page("pages/9_Simulation_Manuelle.py")