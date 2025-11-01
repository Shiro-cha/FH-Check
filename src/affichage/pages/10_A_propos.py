# src/affichage/pages/A_propos.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="À propos du projet", layout="wide")
page = st.sidebar.radio("Navigation", ["Affichage dataset", "Apprentissage", "Démonstration", "Bilan", "Historique", "Autres pages", "A propos"])
# ------------------------------
# Styles CSS mode clair
# ------------------------------
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


/* Titres et description */
.section-title {
    background-color: #e0e0e0;
    color: black;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}

.description-box {
    background-color: #fdfdfd;
    color: black;
    padding: 15px 20px;
    border-radius: 10px;
    font-size: 16px;
    margin-bottom: 20px;
    line-height: 1.5;
}

/* Tableau */
.dataframe tbody tr:nth-child(odd) {
    background-color: #ffffff;
}
.dataframe tbody tr:nth-child(even) {
    background-color: #f9f9f9;
}
.dataframe thead th {
    background-color: #e0e0e0;
    color: black;
    font-weight: bold;
    text-align: center;
}
.dataframe td, .dataframe th {
    border: 1px solid #ccc;
    text-align: center;
    color: black;
    padding: 8px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Titre et description
# ------------------------------
st.markdown('<div class="section-title">À propos du projet FH-Check</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="description-box">'
    'Ce projet a pour objectif de **superviser les liaisons faisceaux hertziens (FH)** grâce à l\'intelligence artificielle.<br>'
    'Il permet de détecter automatiquement les anomalies, de classifier l\'état des liaisons et de visualiser les paramètres clés en temps réel.<br>'
    'Le projet combine la **simulation, l\'apprentissage automatique et l\'interface utilisateur interactive**.'
    '</div>', unsafe_allow_html=True
)

# ------------------------------
# Architecture du projet (graphique)
# ------------------------------
st.markdown('<div class="section-title">Architecture du projet</div>', unsafe_allow_html=True)

fig = go.Figure()

nodes = {
    "Dataset": {"x": 0, "y": 2, "text": "Génération et préparation des données"},
    "AI": {"x": 0, "y": 1, "text": "Apprentissage automatique"},
    "Simulation": {"x": 0, "y": 0, "text": "Simulation et démonstration"},
    "UI": {"x": 2, "y": 1, "text": "Interface utilisateur (Streamlit)"},
}

for key, val in nodes.items():
    fig.add_shape(
        type="rect",
        x0=val["x"]-0.4, x1=val["x"]+0.4,
        y0=val["y"]-0.2, y1=val["y"]+0.2,
        line=dict(color="black"),
        fillcolor="#e0e0e0",
        layer="below"
    )
    fig.add_trace(go.Scatter(
        x=[val["x"]],
        y=[val["y"]],
        text=[val["text"]],
        mode="text",
        textfont=dict(color="black", size=14),
        hoverinfo="text"
    ))

connections = [
    ("Dataset", "AI"),
    ("AI", "Simulation"),
    ("Simulation", "UI"),
]

for start, end in connections:
    fig.add_annotation(
        x=nodes[end]["x"], y=nodes[end]["y"],
        ax=nodes[start]["x"], ay=nodes[start]["y"],
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="black"
    )

fig.update_xaxes(visible=False, range=[-1, 3])
fig.update_yaxes(visible=False, range=[-0.5, 2.5])
fig.update_layout(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    margin=dict(l=20, r=20, t=20, b=20),
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Technologies et Bibliothèques
# ------------------------------
st.markdown('<div class="section-title">Technologies et Bibliothèques</div>', unsafe_allow_html=True)

data = {
    "Outil / Technologie": [
        "Python 3.10", "Streamlit", "Pandas", "NumPy",
        "scikit-learn", "Plotly", "joblib", "Linux Ubuntu"
    ],
    "Description / Usage": [
        "Langage principal du projet",
        "Interface web interactive",
        "Analyse et manipulation de données",
        "Manipulation de tableaux et calculs numériques",
        "Machine Learning : Random Forest, SVM, StandardScaler",
        "Visualisation graphique des paramètres",
        "Sauvegarde et chargement des modèles",
        "Système d'exploitation utilisé"
    ]
}

df_tools = pd.DataFrame(data)

st.dataframe(
    df_tools.style.set_properties(**{
        'background-color': '#ffffff',
        'color': 'black',
        'border-radius': '8px',
        'border': '1px solid #ccc',
        'font-size': '16px',
        'text-align': 'center'
    }).set_table_styles([
        {'selector': 'th', 'props': [('background-color', '#e0e0e0'), ('color', 'black'), ('font-weight','bold')]}
    ])
)

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown("© 2025 - Projet Supervision FH avec Intelligence Artificielle")
