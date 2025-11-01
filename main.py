#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Point d'entrée principal pour l'application de détection d'anomalies dans les liaisons faisceaux hertziens.
"""

import argparse
import sys
import subprocess
from src.simulateur.simulateur import SimulateurFaisceauHertzien
from src.ia.modele import ModeleIA
from src.affichage.cli import AffichageCLI
from src.affichage.graphique import AffichageGraphique
from src.utils.dataset_generator import DatasetGenerator

def parse_arguments():
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(description='Détection d\'anomalies dans les liaisons faisceaux hertziens')
    
    parser.add_argument('--mode', type=str, choices=['cli', 'gui', 'streamlit'], default='cli',
                        help='Mode d\'affichage (cli, gui ou streamlit)')
    
    parser.add_argument('--condition', type=str, 
                        choices=['normal_urbain', 'pluie_urbain', 'brouillard_urbain', 'normal_rural', 'pluie_rural', 'brouillard_rural'],
                        default='normal_urbain',
                        help='Condition initiale de simulation')
    
    parser.add_argument('--generer-dataset', action='store_true',
                        help='Générer un dataset d\'entraînement et quitter')
    
    parser.add_argument('--entrainer-modele', action='store_true',
                        help='Entraîner le modèle sur un dataset généré')
    
    parser.add_argument('--samples', type=int, default=1000,
                        help='Nombre d\'échantillons par condition pour la génération de dataset')
    
    parser.add_argument('--output', type=str, default='dataset.csv',
                        help='Fichier de sortie pour le dataset généré')
    
    return parser.parse_args()

def main():
    """Fonction principale."""
    args = parse_arguments()
    
    # Initialiser le simulateur
    simulateur = SimulateurFaisceauHertzien()
    
    # Génération de dataset
    if args.generer_dataset:
        print(f"Génération d'un dataset avec {args.samples} échantillons par condition...")
        generator = DatasetGenerator(simulateur)
        dataset = generator.generer_dataset(args.samples)
        dataset.to_csv(args.output, index=False)
        print(f"Dataset généré et sauvegardé dans {args.output}")
        return
    
    # Initialiser le modèle
    modele = ModeleIA()
    
    # Entraînement du modèle
    if args.entrainer_modele:
        print("Génération d'un dataset pour l'entraînement...")
        generator = DatasetGenerator(simulateur)
        dataset = generator.generer_dataset(args.samples)
        
        print("Entraînement du modèle...")
        modele.entrainer_et_evaluer(dataset)
        modele.sauvegarder("modele.pkl")
        print("Modèle entraîné et sauvegardé dans modele.pkl")
        return
    
    # Charger ou entraîner un modèle
    try:
        modele.charger("modele.pkl")
        print("Modèle pré-entraîné chargé")
    except FileNotFoundError:
        print("Aucun modèle pré-entraîné trouvé. Entraînement d'un nouveau modèle...")
        generator = DatasetGenerator(simulateur)
        dataset = generator.generer_dataset(1000)
        modele.entrainer_et_evaluer(dataset)
        modele.sauvegarder("modele.pkl")
    
    # Sélection du mode d'affichage
    if args.mode == 'cli':
        affichage = AffichageCLI(simulateur, modele)
        affichage.demarrer(args.condition)
    elif args.mode == 'gui':
        affichage = AffichageGraphique(simulateur, modele)
        affichage.demarrer(args.condition)
    elif args.mode == 'streamlit':
        # Lancer l'application Streamlit
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", 
                "src/affichage/streamlit_app.py", 
                "--", 
                "--condition", args.condition
            ], check=True)
        except subprocess.CalledProcessError:
            print("Erreur lors du lancement de l'application Streamlit")
        except FileNotFoundError:
            print("Streamlit n'est pas installé. Veuillez l'installer avec: pip install streamlit")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt de l'application")
        sys.exit(0)