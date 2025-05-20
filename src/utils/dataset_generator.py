#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module contenant la classe DatasetGenerator pour générer des datasets d'entraînement.
"""

import pandas as pd
from typing import Dict, List, Any
from src.simulateur.simulateur import SimulateurFaisceauHertzien

class DatasetGenerator:
    """
    Classe pour générer des datasets d'entraînement pour le modèle d'IA.
    """
    
    def __init__(self, simulateur: SimulateurFaisceauHertzien):
        """
        Initialise le générateur de dataset.
        
        Args:
            simulateur: Une instance de SimulateurFaisceauHertzien
        """
        self.simulateur = simulateur
    
    def generer_dataset(self, n_samples_per_condition: int = 1000) -> pd.DataFrame:
        """
        Génère un dataset complet pour l'entraînement du modèle.
        
        Args:
            n_samples_per_condition: Nombre d'échantillons à générer par condition
            
        Returns:
            Le dataset complet avec étiquettes
        """
        dfs = []
        conditions = self.simulateur.get_conditions_disponibles()
        
        print(f"Génération du dataset avec {len(conditions)} conditions...")
        
        for i, condition in enumerate(conditions):
            print(f"  Condition {i+1}/{len(conditions)}: {condition}")
            df = self.simulateur.generer_donnees(condition, n_samples_per_condition)
            dfs.append(df)
        
        dataset = pd.concat(dfs, ignore_index=True)
        
        # Ajouter les étiquettes (OK, KO, dégradé)
        print("Ajout des étiquettes...")
        dataset["etat"] = dataset.apply(self.simulateur.classifier_etat_manuel, axis=1)
        
        # Afficher des statistiques sur le dataset
        print("\nStatistiques du dataset:")
        print(f"  Nombre total d'échantillons: {len(dataset)}")
        print("  Distribution des étiquettes:")
        for etat, count in dataset["etat"].value_counts().items():
            print(f"    {etat}: {count} ({count/len(dataset)*100:.2f}%)")
        
        return dataset