#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module contenant la classe SimulateurFaisceauHertzien pour simuler les paramètres
de liaisons faisceaux hertziens dans différentes conditions.
"""

import numpy as np
import pandas as pd
import time
from typing import Dict, List, Any

class SimulateurFaisceauHertzien:
    """
    Classe pour simuler les paramètres de liaisons faisceaux hertziens
    dans différentes conditions environnementales.
    """
    
    def __init__(self):
        """Initialise le simulateur avec les paramètres par défaut pour différentes conditions."""
        # Paramètres de base pour différentes conditions
        self.conditions = {
            "normal_urbain": {
                "rssi_mean": -65, "rssi_std": 3,
                "snr_mean": 25, "snr_std": 2,
                "ber_mean": 0.00001, "ber_std": 0.000005,
                "disponibilite_mean": 99.9, "disponibilite_std": 0.05
            },
            "pluie_urbain": {
                "rssi_mean": -75, "rssi_std": 5,
                "snr_mean": 18, "snr_std": 3,
                "ber_mean": 0.0001, "ber_std": 0.00005,
                "disponibilite_mean": 95.0, "disponibilite_std": 2.0
            },
            "brouillard_urbain": {
                "rssi_mean": -70, "rssi_std": 4,
                "snr_mean": 20, "snr_std": 2.5,
                "ber_mean": 0.00005, "ber_std": 0.000025,
                "disponibilite_mean": 97.0, "disponibilite_std": 1.0
            },
            "normal_rural": {
                "rssi_mean": -60, "rssi_std": 2,
                "snr_mean": 28, "snr_std": 1.5,
                "ber_mean": 0.000005, "ber_std": 0.0000025,
                "disponibilite_mean": 99.95, "disponibilite_std": 0.02
            },
            "pluie_rural": {
                "rssi_mean": -70, "rssi_std": 4,
                "snr_mean": 20, "snr_std": 2.5,
                "ber_mean": 0.00005, "ber_std": 0.000025,
                "disponibilite_mean": 96.0, "disponibilite_std": 1.5
            }
        }
        
        # Seuils pour la classification
        self.seuils = {
            "rssi": {"ok": -70, "degrade": -80},
            "snr": {"ok": 20, "degrade": 15},
            "ber": {"ok": 0.00005, "degrade": 0.0001},
            "disponibilite": {"ok": 99.0, "degrade": 95.0}
        }
    
    def get_conditions_disponibles(self) -> List[str]:
        """Retourne la liste des conditions disponibles."""
        return list(self.conditions.keys())
    
    def generer_donnees(self, condition: str, n_samples: int = 1) -> pd.DataFrame:
        """
        Génère des données simulées pour une condition spécifique.
        
        Args:
            condition: La condition environnementale à simuler
            n_samples: Le nombre d'échantillons à générer
            
        Returns:
            DataFrame contenant les données simulées
        
        Raises:
            ValueError: Si la condition n'est pas reconnue
        """
        if condition not in self.conditions:
            raise ValueError(f"Condition {condition} non reconnue")
            
        params = self.conditions[condition]
        
        data = {
            "timestamp": [time.time() + i for i in range(n_samples)],
            "rssi": np.random.normal(params["rssi_mean"], params["rssi_std"], n_samples),
            "snr": np.random.normal(params["snr_mean"], params["snr_std"], n_samples),
            "ber": np.random.normal(params["ber_mean"], params["ber_std"], n_samples),
            "disponibilite": np.random.normal(params["disponibilite_mean"], params["disponibilite_std"], n_samples),
            "condition": [condition] * n_samples
        }
        
        # Assurer que les valeurs sont dans des plages réalistes
        data["ber"] = np.clip(data["ber"], 0, 1)
        data["disponibilite"] = np.clip(data["disponibilite"], 0, 100)
        
        return pd.DataFrame(data)
    
    def classifier_etat_manuel(self, row: pd.Series) -> str:
        """
        Classifie l'état de la liaison basé sur des règles simples.
        
        Args:
            row: Une ligne de données contenant les paramètres de la liaison
            
        Returns:
            L'état de la liaison: "OK", "DEGRADE" ou "KO"
        """
        if (row["rssi"] >= self.seuils["rssi"]["ok"] and 
            row["snr"] >= self.seuils["snr"]["ok"] and 
            row["ber"] <= self.seuils["ber"]["ok"] and 
            row["disponibilite"] >= self.seuils["disponibilite"]["ok"]):
            return "OK"
        elif (row["rssi"] < self.seuils["rssi"]["degrade"] or 
              row["snr"] < self.seuils["snr"]["degrade"] or 
              row["ber"] > self.seuils["ber"]["degrade"] or 
              row["disponibilite"] < self.seuils["disponibilite"]["degrade"]):
            return "KO"
        else:
            return "DEGRADE"
    
    def ajouter_condition(self, nom: str, parametres: Dict[str, float]) -> None:
        """
        Ajoute une nouvelle condition au simulateur.
        
        Args:
            nom: Le nom de la nouvelle condition
            parametres: Les paramètres de la condition
        """
        self.conditions[nom] = parametres
    
    def modifier_seuils(self, nouveaux_seuils: Dict[str, Dict[str, float]]) -> None:
        """
        Modifie les seuils de classification.
        
        Args:
            nouveaux_seuils: Les nouveaux seuils à utiliser
        """
        self.seuils.update(nouveaux_seuils)