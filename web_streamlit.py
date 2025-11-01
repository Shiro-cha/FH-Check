#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Point d'entrée principal pour l'application Streamlit de détection d'anomalies.
"""

import argparse
import sys
import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.simulateur.simulateur import SimulateurFaisceauHertzien
from src.ia.modele import ModeleIA
from src.affichage.cli import AffichageCLI
from src.utils.dataset_generator import DatasetGenerator

def main():
    """Fonction principale pour l'application Streamlit."""
    st.set_page_config(
        page_title="Détection d'Anomalies - Faisceaux Hertziens",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("Détection d'Anomalies dans les Liaisons Faisceaux Hertziens")
    
    # Initialisation des objets principaux
    simulateur = SimulateurFaisceauHertzien()
    modele = ModeleIA()
    
    # Sidebar pour les contrôles principaux
    with st.sidebar:
        st.header("Configuration")
        
        condition_initiale = st.selectbox(
            "Condition initiale:",
            options=['normal_urbain', 'pluie_urbain', 'brouillard_urbain', 
                    'normal_rural', 'pluie_rural', 'brouillard_rural'],
            index=0
        )
        
        st.header("Actions")
        
        if st.button("Générer Dataset"):
            with st.spinner("Génération du dataset en cours..."):
                generator = DatasetGenerator(simulateur)
                samples = st.slider("Nombre d'échantillons", 100, 5000, 1000)
                dataset = generator.generer_dataset(samples)
                dataset.to_csv("dataset.csv", index=False)
                st.success(f"Dataset généré avec {samples} échantillons et sauvegardé dans dataset.csv")
        
        if st.button("Entraîner Modèle"):
            with st.spinner("Entraînement du modèle en cours..."):
                try:
                    # Charger le dataset ou en générer un nouveau
                    try:
                        dataset = pd.read_csv("dataset.csv")
                    except FileNotFoundError:
                        st.info("Aucun dataset trouvé. Génération d'un nouveau dataset...")
                        generator = DatasetGenerator(simulateur)
                        dataset = generator.generer_dataset(1000)
                    
                    # Entraîner le modèle
                    modele.entrainer_et_evaluer(dataset)
                    modele.sauvegarder("modele.pkl")
                    st.success("Modèle entraîné et sauvegardé avec succès")
                    
                    # Afficher les métriques
                    if hasattr(modele, 'historique_entrainement'):
                        st.line_chart(modele.historique_entrainement)
                        
                except Exception as e:
                    st.error(f"Erreur lors de l'entraînement: {str(e)}")
    
    # Section principale
    tab1, tab2, tab3 = st.tabs(["Simulation", "Modèle IA", "À propos"])
    
    with tab1:
        st.header("Simulation en Temps Réel")
        
        # Initialiser l'état de session
        if 'running' not in st.session_state:
            st.session_state.running = False
        if 'data_history' not in st.session_state:
            st.session_state.data_history = pd.DataFrame()
        if 'etat_actuel' not in st.session_state:
            st.session_state.etat_actuel = "En attente..."
        
        # Contrôles de simulation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Démarrer Simulation", disabled=st.session_state.running):
                st.session_state.running = True
                st.session_state.data_history = pd.DataFrame()
                st.session_state.start_time = pd.Timestamp.now()
        with col2:
            if st.button("Arrêter Simulation", disabled=not st.session_state.running):
                st.session_state.running = False
        
        # Affichage de l'état
        etat = st.session_state.etat_actuel
        if "OK" in etat:
            couleur = "green"
        elif "DEGRADE" in etat:
            couleur = "orange"
        elif "KO" in etat:
            couleur = "red"
        else:
            couleur = "black"
        
        st.markdown(f"<h2 style='color:{couleur};'>{etat}</h2>", unsafe_allow_html=True)
        
        # Simulation en temps réel
        if st.session_state.running:
            # Générer de nouvelles données
            new_data = simulateur.generer_donnees(condition_initiale)
            
            # Ajouter un timestamp relatif
            current_time = pd.Timestamp.now()
            elapsed_time = (current_time - st.session_state.start_time).total_seconds()
            new_data["elapsed_time"] = elapsed_time
            
            # Charger le modèle s'il n'est pas déjà chargé
            try:
                if not hasattr(modele, 'modele_entraine') or not modele.modele_entraine:
                    modele.charger("modele.pkl")
            except FileNotFoundError:
                st.warning("Aucun modèle entraîné trouvé. Veuillez d'abord entraîner un modèle.")
                st.session_state.running = False
                st.rerun()
            
            # Prédire l'état avec le modèle IA
            X = new_data[["rssi", "snr", "ber", "disponibilite"]]
            etat = modele.predire(X)[0]
            new_data["etat"] = etat
            
            # Mettre à jour l'affichage de l'état
            st.session_state.etat_actuel = f"État: {etat}"
            
            # Ajouter à l'historique
            if st.session_state.data_history.empty:
                st.session_state.data_history = new_data
            else:
                st.session_state.data_history = pd.concat(
                    [st.session_state.data_history, new_data], 
                    ignore_index=True
                )
            
            # Limiter l'historique aux 100 derniers points
            if len(st.session_state.data_history) > 100:
                st.session_state.data_history = st.session_state.data_history.tail(100)
        
        # Graphiques
        if not st.session_state.data_history.empty:
            # Utiliser le temps écoulé directement
            elapsed_time = st.session_state.data_history["elapsed_time"]
            
            # Créer des graphiques
            fig, axes = plt.subplots(2, 2, figsize=(10, 8))
            
            axes[0, 0].plot(elapsed_time, st.session_state.data_history["rssi"], 'b-')
            axes[0, 0].set_title("RSSI (dBm)")
            axes[0, 0].set_xlabel("Temps (s)")
            axes[0, 0].set_ylabel("RSSI (dBm)")
            axes[0, 0].grid(True)
            
            axes[0, 1].plot(elapsed_time, st.session_state.data_history["snr"], 'g-')
            axes[0, 1].set_title("SNR (dB)")
            axes[0, 1].set_xlabel("Temps (s)")
            axes[0, 1].set_ylabel("SNR (dB)")
            axes[0, 1].grid(True)
            
            axes[1, 0].plot(elapsed_time, st.session_state.data_history["ber"], 'r-')
            axes[1, 0].set_title("BER")
            axes[1, 0].set_xlabel("Temps (s)")
            axes[1, 0].set_ylabel("BER")
            axes[1, 0].grid(True)
            
            axes[1, 1].plot(elapsed_time, st.session_state.data_history["disponibilite"], 'y-')
            axes[1, 1].set_title("Disponibilité (%)")
            axes[1, 1].set_xlabel("Temps (s)")
            axes[1, 1].set_ylabel("Disponibilité (%)")
            axes[1, 1].grid(True)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Mettre à jour l'interface
            if st.session_state.running:
                time.sleep(0.5)
                st.rerun()
    
    with tab2:
        st.header("Informations sur le Modèle IA")
        
        # Charger le modèle s'il existe
        try:
            modele.charger("modele.pkl")
            st.success("Modèle chargé avec succès")
            
            # Afficher les informations du modèle
            if hasattr(modele, 'precision'):
                st.metric("Précision du modèle", f"{modele.precision:.2%}")
            
            if hasattr(modele, 'matrice_confusion'):
                st.subheader("Matrice de Confusion")
                fig, ax = plt.subplots()
                sns.heatmap(modele.matrice_confusion, annot=True, fmt='d', ax=ax)
                ax.set_xlabel('Prédiction')
                ax.set_ylabel('Vérité terrain')
                st.pyplot(fig)
                
        except FileNotFoundError:
            st.warning("Aucun modèle entraîné trouvé. Veuillez d'abord entraîner un modèle.")
    
    with tab3:
        st.header("À propos de cette Application")
        st.markdown("""
        Cette application permet de détecter les anomalies dans les liaisons faisceaux hertziens
        en utilisant l'intelligence artificielle.
        
        **Fonctionnalités:**
        - Simulation de différentes conditions environnementales
        - Génération de datasets pour l'entraînement
        - Entraînement de modèles de machine learning
        - Détection en temps réel des anomalies
        - Visualisation des métriques de performance
        
        **Technologies utilisées:**
        - Python
        - Streamlit pour l'interface
        - Scikit-learn pour le machine learning
        - Matplotlib pour la visualisation
        """)

if __name__ == "__main__":
    main()