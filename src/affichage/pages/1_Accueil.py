#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st

# --------------------------------------------------
# Config de la page principale
# --------------------------------------------------
st.set_page_config(
    page_title="FH-Check - Supervision FH",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Styles modernes allégés
# --------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: #eceef2;
    border-right: 1px solid #e0e0e0;
    padding-top: 10px;
}
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
.stApp, .main, .block-container {
    background: #f9f9f9 !important;
    padding: 15px 20px;
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

/* --- Feature cards --- */
.feature-card {
    background: #fff;
    border-radius: 12px;
    padding: 30px;                  /* plus d’espace intérieur */
    text-align: center;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    transition: 0.3s ease;
    height: 230px;                  /* hauteur augmentée */
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.feature-card h3 { 
    color: #6a0dad; 
    font-size: 20px;                /* titre plus grand */
    margin-bottom: 10px; 
}
.feature-card p { 
    color: #555; 
    font-size: 15px;                /* texte un peu plus grand */
    line-height: 1.5; 
}
.feature-card:hover { 
    transform: translateY(-6px); 
    box-shadow: 0 6px 18px rgba(0,0,0,0.12); 
}

/* --- User Flow Boxes --- */
.user-flow-box {
    flex: 1 1 22%;
    background: #fff;
    border-radius: 10px;
    margin: 8px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    transition: 0.25s ease;
}
.user-flow-box:hover { transform: translateY(-3px); box-shadow: 0 3px 12px rgba(0,0,0,0.1); }
.user-flow-box b { color: #6a0dad; font-size: 15px; }
.user-flow-box small { color: #666; display: block; margin-top: 5px; font-size: 12px; }


/* --- Bouton central --- */
div.stButton > button {
    background: #6a0dad;
    color: #fff;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
    transition: 0.3s;
}
div.stButton > button:hover {
    background: #4b007f;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Grand titre
# --------------------------------------------------
st.markdown("""
<div class="title-card">
    FH-Check
    <div class="title-sub">Supervision intelligente des liaisons hertziennes</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Présentation du projet
# --------------------------------------------------
st.markdown("""
<p style="text-align:justify; font-size:15px; color:#333;">
<strong>FH-Check</strong> est une plateforme intelligente de supervision des liaisons faisceaux hertziens. 
Elle permet de <strong>détecter automatiquement</strong> les anomalies, 
de <strong>classifier les états de liaison</strong>, 
et de <strong>visualiser en temps réel</strong> les indicateurs clés de performance.
</p>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Parcours utilisateur
# --------------------------------------------------
st.markdown("""
<div style="display:flex; justify-content:space-around; flex-wrap:wrap;">
    <div class="user-flow-box">
        <b>Charger le Dataset</b>
        <small>Données FH collectées</small>
    </div>
    <div class="user-flow-box">
        <b>Entraîner le Modèle</b>
        <small>IA : Random Forest, SVM, KNN</small>
    </div>
    <div class="user-flow-box">
        <b>Démonstration</b>
        <small>Conditions réelles FH</small>
    </div>
    <div class="user-flow-box">
        <b>Résultats</b>
        <small>Analyse & classification</small>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Fonctionnalités principales
# --------------------------------------------------
st.markdown('<h4 style="margin-top:25px;">Fonctionnalités principales</h4>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
features = [
    ("Détection en temps réel", "Surveillance continue des états FH avec calcul instantané du RSSI, SNR, BER et disponibilité."),
    ("Visualisation graphique", "Affichage interactif et dynamique des variations FH sous forme de courbes et graphiques intuitifs."),
    ("Classification via IA", "Analyse intelligente permettant de classer automatiquement les états : OK, Dégradé ou KO."),
    ("Bilan global", "Résumé avec pourcentage de disponibilité et décision finale sur les performances du lien.")
]
for col, (title, text) in zip([col1, col2, col3, col4], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# Bouton central
# --------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Commencer la supervision"):
    st.switch_page("pages/2_Dataset.py")