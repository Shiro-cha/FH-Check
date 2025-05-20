#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module contenant la classe AffichageGraphique pour l'interface graphique.
"""

import time
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from src.simulateur.simulateur import SimulateurFaisceauHertzien
from src.ia.modele import ModeleIA

class AffichageGraphique:
    """
    Classe pour l'affichage graphique des résultats de la simulation.
    """
    
    def __init__(self, simulateur: SimulateurFaisceauHertzien, modele: ModeleIA):
        """
        Initialise l'affichage graphique.
        
        Args:
            simulateur: Une instance de SimulateurFaisceauHertzien
            modele: Une instance de ModeleIA
        """
        self.simulateur = simulateur
        self.modele = modele
        self.running = False
        self.data_history = pd.DataFrame()
        self.simulation_thread = None
    
    def creer_interface(self) -> None:
        """Crée l'interface utilisateur graphique."""
        self.root = tk.Tk()
        self.root.title("Détection d'Anomalies dans les Liaisons Faisceaux Hertziens")
        self.root.geometry("1200x800")
        
        # Variables
        self.condition_actuelle = tk.StringVar(value="normal_urbain")
        self.etat_actuel = tk.StringVar(value="En attente...")
        
        # Frame principale
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de contrôle
        control_frame = ttk.LabelFrame(main_frame, text="Contrôles", padding=10)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Sélection de la condition
        ttk.Label(control_frame, text="Condition:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        condition_combo = ttk.Combobox(control_frame, textvariable=self.condition_actuelle, 
                                      values=self.simulateur.get_conditions_disponibles())
        condition_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Boutons de contrôle
        self.start_button = ttk.Button(control_frame, text="Démarrer", command=self.demarrer_simulation)
        self.start_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.stop_button = ttk.Button(control_frame, text="Arrêter", command=self.arreter_simulation, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=3, padx=5, pady=5)
        
        # Affichage de l'état
        etat_frame = ttk.LabelFrame(main_frame, text="État de la Liaison", padding=10)
        etat_frame.pack(fill=tk.X, pady=10)
        
        self.etat_label = ttk.Label(etat_frame, textvariable=self.etat_actuel, font=("Arial", 16, "bold"))
        self.etat_label.pack(pady=10)
        
        # Frame pour les graphiques
        graph_frame = ttk.LabelFrame(main_frame, text="Graphiques en Temps Réel", padding=10)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Création des graphiques
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 6))
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configuration des graphiques
        self.axes[0, 0].set_title("RSSI (dBm)")
        self.axes[0, 0].set_xlabel("Temps (s)")
        self.axes[0, 0].set_ylabel("RSSI (dBm)")
        self.rssi_line, = self.axes[0, 0].plot([], [], 'b-')
        
        self.axes[0, 1].set_title("SNR (dB)")
        self.axes[0, 1].set_xlabel("Temps (s)")
        self.axes[0, 1].set_ylabel("SNR (dB)")
        self.snr_line, = self.axes[0, 1].plot([], [], 'g-')
        
        self.axes[1, 0].set_title("BER")
        self.axes[1, 0].set_xlabel("Temps (s)")
        self.axes[1, 0].set_ylabel("BER")
        self.ber_line, = self.axes[1, 0].plot([], [], 'r-')
        
        self.axes[1, 1].set_title("Disponibilité (%)")
        self.axes[1, 1].set_xlabel("Temps (s)")
        self.axes[1, 1].set_ylabel("Disponibilité (%)")
        self.disponibilite_line, = self.axes[1, 1].plot([], [], 'y-')
    
    def demarrer_simulation(self) -> None:
        """Démarre la simulation."""
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Réinitialiser l'historique des données
        self.data_history = pd.DataFrame()
        
        # Démarrer la simulation dans un thread séparé
        self.simulation_thread = threading.Thread(target=self.executer_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()
    
    def arreter_simulation(self) -> None:
        """Arrête la simulation."""
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def executer_simulation(self) -> None:
        """Exécute la simulation en continu."""
        while self.running:
            # Générer de nouvelles données
            condition = self.condition_actuelle.get()
            new_data = self.simulateur.generer_donnees(condition)
            
            # Prédire l'état avec le modèle IA
            X = new_data[["rssi", "snr", "ber", "disponibilite"]]
            etat = self.modele.predire(X)[0]
            new_data["etat"] = etat
            
            # Mettre à jour l'affichage de l'état
            self.etat_actuel.set(f"État: {etat}")
            
            # Changer la couleur de l'étiquette en fonction de l'état
            if etat == "OK":
                self.etat_label.config(foreground="green")
            elif etat == "DEGRADE":
                self.etat_label.config(foreground="orange")
            else:  # KO
                self.etat_label.config(foreground="red")
            
            # Ajouter à l'historique
            if self.data_history.empty:
                self.data_history = new_data
            else:
                self.data_history = pd.concat([self.data_history, new_data], ignore_index=True)
            
            # Limiter l'historique aux 100 derniers points
            if len(self.data_history) > 100:
                self.data_history = self.data_history.tail(100)
            
            # Mettre à jour les graphiques
            self.mettre_a_jour_graphiques()
            
            # Attendre un peu
            time.sleep(0.5)
    
    def mettre_a_jour_graphiques(self) -> None:
        """Met à jour les graphiques avec les données actuelles."""
        if len(self.data_history) == 0:
            return
            
        # Calculer le temps relatif
        start_time = self.data_history["timestamp"].min()
        relative_time = self.data_history["timestamp"] - start_time
        
        # Mettre à jour les données des graphiques
        self.rssi_line.set_data(relative_time, self.data_history["rssi"])
        self.snr_line.set_data(relative_time, self.data_history["snr"])
        self.ber_line.set_data(relative_time, self.data_history["ber"])
        self.disponibilite_line.set_data(relative_time, self.data_history["disponibilite"])
        
        # Ajuster les limites des axes
        for ax, param in zip([self.axes[0, 0], self.axes[0, 1], self.axes[1, 0], self.axes[1, 1]], 
                            ["rssi", "snr", "ber", "disponibilite"]):
            ax.relim()
            ax.autoscale_view()
        
        # Redessiner le canvas
        self.canvas.draw_idle()
    
    def demarrer(self, condition_initiale: str) -> None:
        """
        Démarre l'interface graphique.
        
        Args:
            condition_initiale: La condition initiale de simulation
        """
        self.creer_interface()
        self.condition_actuelle.set(condition_initiale)
        self.root.mainloop()