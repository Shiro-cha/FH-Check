#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module contenant la classe AffichageCLI pour l'interface en ligne de commande.
"""

import time
import sys
import pandas as pd
from typing import Dict, List, Any
from src.simulateur.simulateur import SimulateurFaisceauHertzien
from src.ia.modele import ModeleIA

class AffichageCLI:
    """
    Classe pour l'affichage en ligne de commande des résultats de la simulation.
    """
    
    def __init__(self, simulateur: SimulateurFaisceauHertzien, modele: ModeleIA):
        """
        Initialise l'affichage CLI.
        
        Args:
            simulateur: Une instance de SimulateurFaisceauHertzien
            modele: Une instance de ModeleIA
        """
        self.simulateur = simulateur
        self.modele = modele
        self.running = False
        self.data_history = pd.DataFrame()
    
    def afficher_parametres(self, data: pd.DataFrame) -> None:
        """
        Affiche les paramètres de la liaison.
        
        Args:
            data: Les données à afficher
        """
        # Extraire les valeurs
        rssi = data["rssi"].values[0]
        snr = data["snr"].values[0]
        ber = data["ber"].values[0]
        disponibilite = data["disponibilite"].values[0]
        condition = data["condition"].values[0]
        etat = data["etat"].values[0]
        
        # Déterminer les couleurs pour l'état
        if etat == "OK":
            etat_color = "\033[92m"  # Vert
        elif etat == "DEGRADE":
            etat_color = "\033[93m"  # Jaune
        else:  # KO
            etat_color = "\033[91m"  # Rouge
        
        reset_color = "\033[0m"
        
        # Afficher les paramètres
        print("\033[H\033[J", end="")  # Effacer l'écran
        print("=" * 50)
        print(f"SIMULATION DE LIAISON FAISCEAU HERTZIEN - {condition.upper()}")
        print("=" * 50)
        print(f"RSSI: {rssi:.2f} dBm")
        print(f"SNR: {snr:.2f} dB")
        print(f"BER: {ber:.8f}")
        print(f"Disponibilité: {disponibilite:.2f}%")
        print("-" * 50)
        print(f"ÉTAT: {etat_color}{etat}{reset_color}")
        print("=" * 50)
        print("\nAppuyez sur Ctrl+C pour quitter ou entrez une nouvelle condition:")
        for i, cond in enumerate(self.simulateur.get_conditions_disponibles()):
            print(f"{i+1}. {cond}")
    
    def demarrer(self, condition_initiale: str) -> None:
        """
        Démarre la simulation en mode CLI.
        
        Args:
            condition_initiale: La condition initiale de simulation
        """
        self.running = True
        condition_actuelle = condition_initiale
        
        print("Démarrage de la simulation en mode CLI...")
        print("Appuyez sur Ctrl+C pour quitter.")
        
        try:
            while self.running:
                # Générer de nouvelles données
                new_data = self.simulateur.generer_donnees(condition_actuelle)
                
                # Prédire l'état avec le modèle IA
                X = new_data[["rssi", "snr", "ber", "disponibilite"]]
                etat = self.modele.predire(X)[0]
                new_data["etat"] = etat
                
                # Ajouter à l'historique
                self.data_history = pd.concat([self.data_history, new_data], ignore_index=True)
                
                # Limiter l'historique aux 100 derniers points
                if len(self.data_history) > 100:
                    self.data_history = self.data_history.tail(100)
                
                # Afficher les paramètres
                self.afficher_parametres(new_data)
                
                # Attendre l'entrée utilisateur avec timeout
                import select
                i, o, e = select.select([sys.stdin], [], [], 1)
                
                if i:
                    user_input = sys.stdin.readline().strip()
                    try:
                        index = int(user_input) - 1
                        conditions = self.simulateur.get_conditions_disponibles()
                        if 0 <= index < len(conditions):
                            condition_actuelle = conditions[index]
                            print(f"Changement de condition: {condition_actuelle}")
                    except ValueError:
                        pass
                
                # Attendre un peu
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nArrêt de la simulation")
            self.running = False