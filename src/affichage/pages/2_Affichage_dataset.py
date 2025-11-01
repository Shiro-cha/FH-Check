# src/app/streamlit_app.py
import streamlit as st
import pandas as pd
import os


# Sidebar navigation pour la page Affichage dataset
page = st.sidebar.radio("Navigation", ["Affichage dataset", "Autres pages"])
# --------------------------------------------------
# Styles personnalisés mode clair
# --------------------------------------------------
st.markdown("""
<style>
/* --- Sidebar --- */
[data-testid="stSidebar"] {
    background: #eceef2;
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


/* --- Grand titre --- */
.title-card {
    background: #f4edf9;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    color: #6a0dad;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.title-sub {
    font-size: 16px;
    font-weight: 500;
    margin-top: 5px;
    color: #444;
}

/* Bouton central dataset (violet, texte blanc, petit, carré arrondi) */
.dataset-button {
    display: inline-block;
    padding: 10px 20px;        /* moins de padding → plus petit bouton */
    margin: 15px 0;
    font-size: 14px;            /* texte plus petit */
    font-weight: 600;
    color: #ffffff;             /* texte blanc */
    background: #6a0dad;        /* violet */
    border-radius: 8px;         /* coins arrondis modérés */
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    border: none;               /* pas de bordure visible */
}

.dataset-button:hover {
    background: #4b007f;        /* violet foncé au survol */
    transform: translateY(-2px) scale(1.02);  /* léger effet flottant */
}


/* Tableau clair amélioré */
table {
    border-collapse: collapse;
    width: 100%;
    text-align: center;
    background-color: #ffffff;  /* fond du tableau blanc */
}

table th, table td {
    border: 1px solid #000000;  /* bordures noires pour tout le tableau */
    padding: 8px 12px;
    color: #222;
    background-color: #ffffff;   /* fond des cellules blanc */
}

table th {
    font-weight: bold;
    background-color: #f4edf9;  /* fond violet très clair pour l'en-tête */
    color: #000000;              /* texte noir */
}

table tr:hover td {
    background-color: #f5f5f5;  /* léger gris au survol */
}

/* Labels clair */
label, .css-1aumxhk label, .stText label, .stSelectbox label, .stSlider label {
    color: #333 !important;
}


</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Bouton pour afficher le dataset
# --------------------------------------------------
st.markdown('<div class="dataset-button">Afficher le Dataset</div>', unsafe_allow_html=True)
st.markdown("---")

# --------------------------------------------------
# Sidebar pour filtrage interactif
# --------------------------------------------------
st.sidebar.header("Filtres")
dataset_path = os.path.join("data", "dataset_FH.csv")

if os.path.exists(dataset_path):
    df = pd.read_csv(dataset_path)

    # Filtres
    conditions = df["Condition"].unique().tolist()
    selected_conditions = st.sidebar.multiselect("Filtrer par condition", options=conditions, default=conditions)

    etats = df["Etat"].unique().tolist()
    selected_etat = st.sidebar.multiselect("Filtrer par statut", options=etats, default=etats)

    # Appliquer filtres
    filtered_df = df[df["Condition"].isin(selected_conditions) & df["Etat"].isin(selected_etat)]

    # Coloration conditionnelle
    def color_status(val):
        if val == "OK":
            color = '#00e676'
        elif val == "Dégradé":
            color = '#ffea00'
        else:
            color = '#ff1744'
        return f'color: {color}; font-weight: bold;'


    styled_df = filtered_df.style.applymap(color_status, subset=['Etat']) \
        .set_table_styles([
        {'selector': 'th',
         'props': [
             ('background-color', '#f4edf9 !important'),  # fond violet très clair
             ('color', '#555 !important'),  # texte gris
             ('font-weight', 'normal'),  # texte non gras
             ('border', '1px solid #000000 !important'),  # bordure normale
             ('text-align', 'center')
         ]},
        {'selector': 'td',
         'props': [
             ('border', '1px solid #000000 !important'),
             ('text-align', 'center')
         ]},
        {'selector': 'tr:hover',
         'props': [
             ('background-color', '#f5f5f5 !important')  # survol gris clair
         ]}
    ])

    # Affichage tableau interactif
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)

    st.subheader("Aperçu du dataset filtré")
    st.dataframe(filtered_df, width=1600, height=600)
    st.markdown(f"**Nombre de lignes affichées :** {len(filtered_df)}")
else:
    st.error(f"Le fichier {dataset_path} n'a pas été trouvé. Génère d'abord le dataset.")

# --------------------------------------------------
# Bouton Next pour la page suivante
# --------------------------------------------------
if st.button("Next"):
    st.switch_page("pages/4_Apprentissage.py")
