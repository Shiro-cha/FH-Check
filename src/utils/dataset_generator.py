#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from tqdm import tqdm  # pip install tqdm pour barre de progression
import os
import sys

# Ajouter src au PYTHONPATH pour importer le simulateur
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.simulateur.simulateur import SimulateurFaisceauHertzien


class DatasetGenerator:
    """
    Génère un dataset complet à partir du simulateur FH
    """

    def __init__(self, simulateur: SimulateurFaisceauHertzien):
        self.simulateur = simulateur

    def generer_dataset(self, n_samples_per_condition=1000, save_path="dataset_FH.csv"):
        """
        Génère un dataset pour toutes les conditions disponibles.
        """
        all_data = []

        conditions = self.simulateur.get_conditions_disponibles()
        print(f"Génération du dataset FH pour {len(conditions)} conditions...")

        for cond in conditions:
            print(f"Simuler condition : {cond}")
            for _ in tqdm(range(n_samples_per_condition)):
                sample = self.simulateur.simulate_fh()
                sample["Condition"] = cond  # Forcer la condition
                all_data.append(sample)

        df = pd.DataFrame(all_data)

        # Sauvegarde CSV
        df.to_csv(save_path, index=False)
        print(f"Dataset généré avec succès : {save_path}")
        return df


# --------------------------
# Lancer directement le générateur
# --------------------------
if __name__ == "__main__":
    simulateur = SimulateurFaisceauHertzien()
    generator = DatasetGenerator(simulateur)
    # 1000 échantillons par condition (modifiable)
    generator.generer_dataset(n_samples_per_condition=500)
