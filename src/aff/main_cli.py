#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import pandas as pd
from tabulate import tabulate  # pip install tabulate
import select
import os

# Ajouter le dossier parent dans sys.path pour trouver le package simulateur
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.simulateur.simulateur import SimulateurFaisceauHertzien


class CLISimulateurFH:
    """
    CLI interactif pour simuler des liaisons FH
    """

    def __init__(self, simulateur: SimulateurFaisceauHertzien):
        self.simulateur = simulateur
        self.running = False
        self.data_history = pd.DataFrame()

    @staticmethod
    def afficher_parametres(df: pd.DataFrame):
        """
        Affiche les derniers points simulés sous forme de tableau
        """

        def color_etat(etat):
            if etat == "OK":
                return f"\033[92m{etat}\033[0m"
            elif etat == "Dégradé":
                return f"\033[93m{etat}\033[0m"
            else:
                return f"\033[91m{etat}\033[0m"

        display_df = df.copy()
        display_df["Etat"] = display_df["Status"].apply(color_etat)

        # Effacer l'écran et afficher le tableau
        print("\033[H\033[J", end="")
        print("=" * 80)
        print("SIMULATION LIAISON FAISCEAU HERTZIEN (FH)".center(80))
        print("=" * 80)
        print(tabulate(display_df, headers='keys', tablefmt='fancy_grid', showindex=False))
        print("=" * 80)
    def demarrer(self):
        """
        Démarre la simulation CLI
        """
        self.running = True
        print("Démarrage de la simulation CLI...")
        print("Tapez Ctrl+C pour quitter.\n")

        # Choix de la condition initiale
        conditions = self.simulateur.get_conditions_disponibles()
        print("Choisissez une condition initiale :")
        for i, cond in enumerate(conditions):
            print(f"{i+1}. {cond}")

        try:
            user_input = input("\nNuméro de la condition : ").strip()
            index = int(user_input) - 1
            if 0 <= index < len(conditions):
                condition_actuelle = conditions[index]
            else:
                print("Numéro invalide, utilisation de la première condition")
                condition_actuelle = conditions[0]
        except ValueError:
            print("Entrée invalide, utilisation de la première condition")
            condition_actuelle = conditions[0]

        try:
            while self.running:
                # Générer un échantillon
                sample = self.simulateur.simulate_fh()
                sample["Condition"] = condition_actuelle

                # Ajouter à l'historique et garder les 20 derniers points
                self.data_history = pd.concat([self.data_history, pd.DataFrame([sample])], ignore_index=True)
                display_data = self.data_history.tail(20)

                # Afficher le tableau
                self.afficher_parametres(display_data)

                # Gestion changement de condition
                i, o, e = select.select([sys.stdin], [], [], 1)
                if i:
                    user_input = sys.stdin.readline().strip()
                    try:
                        idx = int(user_input) - 1
                        if 0 <= idx < len(conditions):
                            condition_actuelle = conditions[idx]
                            print(f"Changement de condition : {condition_actuelle}")
                            time.sleep(0.5)
                        else:
                            print("Numéro invalide !")
                    except ValueError:
                        print("Entrée invalide !")

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nArrêt de la simulation CLI.")
            self.running = False


# --------------------------
# Lancer le CLI
# --------------------------
if __name__ == "__main__":
    sim = SimulateurFaisceauHertzien()
    cli = CLISimulateurFH(sim)
    cli.demarrer()
