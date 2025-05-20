#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Point d'entrée principal pour l'application de détection d'anomalies dans les liaisons faisceaux hertziens.
"""

import argparse
import sys
from src.simulateur.simulateur import SimulateurFaisceauHertzien
from src.ia.modele import ModeleIA
from src.affichage.cli import AffichageCLI
from src.affichage.graphique import AffichageGraphique
from src.utils.dataset_generator import DatasetGenerator

def parse_arguments():
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(description='Détection d\'anomalies dans les liaisons faisceaux hertziens')
    
    parser.add_argument('--mode', type=str, choices=['cli', 'gui'], default='cli',
                        help='Mode d\'affichage (cli ou gui)')
    
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
    

    simulateur = SimulateurFaisceauHertzien()
    

    if args.generer_dataset:
        print(f"Génération d'un dataset avec {args.samples} échantillons par condition...")
        generator = DatasetGenerator(simulateur)
        dataset = generator.generer_dataset(args.samples)
        dataset.to_csv(args.output, index=False)
        print(f"Dataset généré et sauvegardé dans {args.output}")
        return
    

    modele = ModeleIA()
    

    if args.entrainer_modele:
        print("Génération d'un dataset pour l'entraînement...")
        generator = DatasetGenerator(simulateur)
        dataset = generator.generer_dataset(args.samples)
        
        print("Entraînement du modèle...")
        modele.entrainer_et_evaluer(dataset)
        modele.sauvegarder("modele.pkl")
        print("Modèle entraîné et sauvegardé dans modele.pkl")
        return
    

    try:
        modele.charger("modele.pkl")
        print("Modèle pré-entraîné chargé")
    except FileNotFoundError:
        print("Aucun modèle pré-entraîné trouvé. Entraînement d'un nouveau modèle...")
        generator = DatasetGenerator(simulateur)
        dataset = generator.generer_dataset(1000)
        modele.entrainer_et_evaluer(dataset)
        modele.sauvegarder("modele.pkl")
    
  
    if args.mode == 'cli':
        affichage = AffichageCLI(simulateur, modele)
        affichage.demarrer(args.condition)
    else: 
        affichage = AffichageGraphique(simulateur, modele)
        affichage.demarrer(args.condition)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt de l'application")
        sys.exit(0)