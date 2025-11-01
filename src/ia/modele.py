#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module contenant la classe ModeleIA pour la classification de l'état des liaisons faisceaux hertziens.
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from typing import Dict, List, Tuple, Any


class ModeleIA:
    """
    Classe pour la classification de l'état des liaisons faisceaux hertziens
    à l'aide d'un modèle d'apprentissage automatique.
    """

    def __init__(self):
        """Initialise le modèle d'IA."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.trained = False
        self.features = ["rssi", "snr", "ber", "disponibilite"]
        self.target = "etat"

    def entrainer(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Entraîne le modèle sur les données fournies.

        Args:
            X: Les caractéristiques d'entraînement
            y: Les étiquettes d'entraînement
        """
        self.model.fit(X, y)
        self.trained = True

    def predire(self, X: pd.DataFrame) -> np.ndarray:
        """
        Prédit l'état de la liaison.

        Args:
            X: Les caractéristiques pour la prédiction

        Returns:
            Les prédictions du modèle

        Raises:
            ValueError: Si le modèle n'a pas encore été entraîné
        """
        if not self.trained:
            raise ValueError("Le modèle n'a pas encore été entraîné")
        return self.model.predict(X)

    def evaluer(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Évalue les performances du modèle.

        Args:
            X: Les caractéristiques de test
            y: Les étiquettes de test

        Returns:
            Un rapport de classification

        Raises:
            ValueError: Si le modèle n'a pas encore été entraîné
        """
        if not self.trained:
            raise ValueError("Le modèle n'a pas encore été entraîné")
        predictions = self.model.predict(X)
        return classification_report(y, predictions, output_dict=True)

    def entrainer_et_evaluer(self, dataset: pd.DataFrame) -> Dict[str, Any]:
        """
        Entraîne et évalue le modèle sur le dataset fourni.

        Args:
            dataset: Le dataset complet avec caractéristiques et étiquettes

        Returns:
            Un rapport de classification
        """
        # Préparation des données
        X = dataset[self.features]
        y = dataset[self.target]

        # Division train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entraînement
        self.entrainer(X_train, y_train)

        # Évaluation
        rapport = self.evaluer(X_test, y_test)

        # Afficher le rapport
        print("Rapport de classification:")
        for classe in rapport:
            if classe in ['OK', 'DEGRADE', 'KO']:
                print(f"  {classe}:")
                print(f"    Précision: {rapport[classe]['precision']:.4f}")
                print(f"    Rappel: {rapport[classe]['recall']:.4f}")
                print(f"    F1-score: {rapport[classe]['f1-score']:.4f}")

        print(f"Précision globale: {rapport['accuracy']:.4f}")

        return rapport

    def sauvegarder(self, chemin_fichier: str) -> None:
        """
        Sauvegarde le modèle entraîné dans un fichier.

        Args:
            chemin_fichier: Le chemin du fichier où sauvegarder le modèle

        Raises:
            ValueError: Si le modèle n'a pas encore été entraîné
        """
        if not self.trained:
            raise ValueError("Le modèle n'a pas encore été entraîné")

        with open(chemin_fichier, 'wb') as f:
            pickle.dump(self.model, f)

    def charger(self, chemin_fichier: str) -> None:
        """
        Charge un modèle entraîné depuis un fichier.

        Args:
            chemin_fichier: Le chemin du fichier contenant le modèle

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
        """
        with open(chemin_fichier, 'rb') as f:
            self.model = pickle.load(f)
        self.trained = True