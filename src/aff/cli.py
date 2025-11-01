#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import pandas as pd
from tabulate import tabulate  # pip install tabulate

from src.simulateur.simulateur import SimulateurFaisceauHertzien
from src.ia.modele import ModeleIA


class AffichageCLI:
    """
    Interface CLI interactive pour le simulateur FH
    """

    def __init__(self, simulateur: SimulateurFaisceauHertzien, modele: ModeleIA):
        self.simulateur = simulateur
        self.modele = modele
        self.running = False
        self.data_history = pd.DataFrame()

    def afficher_parametres(self, data: pd.DataFrame) -> None:
        """
        Affiche les derniers points simulés sous forme de tableau
        """

        # Ajouter la colonne Etat avec couleurs ANSI
        def color_etat(etat):
            if etat == "OK":
                return f"\033[92m{etat}\033[0m"
            elif etat == "Dégradé":
                return f"\033[93m{etat}\033[0m"
            else:
                return f"\033[91m{etat}\033[0m"

        df = data.copy()
        df["Etat"] = df["etat"].apply(color_etat)

        # Afficher tableau dans CLI
        print("\033[H\033[J", end="")  # Effacer écran
        print("=" * 80)
        print("SIMULATION LIAISON FAISCEAU HERTZIEN (FH)".center(80))
        print("=" * 80)
        print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
        print("=" * 80)
        print("\nTapez le numéro de la condition pour changer ou Ctrl+C pour quitter:")
        for i, cond in enumerate(self.simulateur.get_conditions_disponibles()):
            print(f"{i + 1}. {cond}")

    def demarrer(self, condition_initiale: str) -> None:
        """
        Démarre la simulation CLI
        """
        self.running = True
        condition_actuelle = condition_initiale

        print("Démarrage de la simulation CLI...")
        print("Appuyez sur Ctrl+C pour quitter.\n")

        try:
            while self.running:
                # Générer de nouvelles données
                new_data = self.simulateur.generer_donnees(condition_actuelle)

                # Préparer les données pour IA
                X = new_data[["rssi", "snr", "ber", "disponibilite"]]

                # Prédire l'état via IA
                etat = self.modele.predire(X)[0]
                new_data["etat"] = etat

                # Ajouter à l'historique et limiter à 20 derniers points pour tableau
                self.data_history = pd.concat([self.data_history, new_data], ignore_index=True)
                display_data = self.data_history.tail(20)

                # Afficher
                self.afficher_parametres(display_data)

                # Gestion entrée utilisateur avec timeout 1s
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
                            time.sleep(0.5)
                    except ValueError:
                        print("Entrée invalide !")

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nArrêt de la simulation CLI.")
            self.running = False
