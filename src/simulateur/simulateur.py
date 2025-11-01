#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

class SimulateurFaisceauHertzien:
    """
    Simulateur de liaison FH selon distance, météo, urbain/rural,
    modulation, puissance et antenne, prêt pour dataset IA.
    """

    def __init__(self):
        self.conditions = [
            "Normal_Rural", "Normal_Urbain", "Pluie_Rural", "Pluie_Urbain",
            "Brouillard_Rural", "Brouillard_Urbain", "Cyclone", "Orage",
            "Foret_dense", "Vent_fort", "Montagneux"
        ]
        self.frequencies = [4,6,8,11,13,18,23,26,32,38]  # GHz
        self.eband = [70,80]  # GHz courte distance <5km
        self.modulations = ["BPSK","QPSK","8PSK","16-QAM","32-QAM","64-QAM","256-QAM"]
        self.bandwidths = [14,28,56,112,224]  # MHz

    def simulate_fh(self) -> dict:
        # Choix aléatoire condition et distance
        cond = np.random.choice(self.conditions)
        distance = np.random.uniform(0.5,50)  # km

        # Fréquence
        if distance <= 5:
            freq = np.random.choice(self.frequencies + self.eband)
        else:
            freq = np.random.choice(self.frequencies)

        # Bandwidth
        bw = np.random.choice(self.bandwidths)

        # Tx Power et Gain selon distance
        if distance <= 5:
            tx_power = np.random.uniform(17,20)
            gain = np.random.uniform(20,25)
        elif distance <= 20:
            tx_power = np.random.uniform(20,24)
            gain = np.random.uniform(25,30)
        else:
            tx_power = np.random.uniform(24,27)
            gain = np.random.uniform(30,40)

        # RSSI de base
        rssi = tx_power + gain - distance*2 - np.random.uniform(0,2)

        # Ajustements selon conditions
        if "Urbain" in cond:
            rssi -= np.random.uniform(5,10)  # pénalité RSSI urbain
        if "Pluie" in cond or "Brouillard" in cond:
            rssi -= np.random.uniform(2,5)
        if "Foret" in cond or "Montagneux" in cond:
            rssi -= np.random.uniform(3,7)
        if "Cyclone" in cond or "Orage" in cond:
            rssi -= np.random.uniform(10,15)
        if "Vent_fort" in cond:
            rssi -= np.random.uniform(0,3)

        # SNR corrélé au RSSI, avec bruit aléatoire
        snr = max(0, rssi + np.random.uniform(0,10))

        # BER corrélé au SNR et conditions
        if snr >= 20:
            ber = np.random.uniform(0,1e-6)
        elif snr >= 10:
            ber = np.random.uniform(1e-6,1e-3)
        else:
            ber = np.random.uniform(1e-3,1e-1)

        # Renforcer BER si conditions difficiles + distance longue
        if ("Pluie" in cond or "Brouillard" in cond or "Urbain" in cond or "Foret" in cond or "Montagneux" in cond) and distance > 20:
            ber *= np.random.uniform(1.5,3)

        # Disponibilité selon scénario combiné
        if "Cyclone" in cond or "Orage" in cond:
            availability = np.random.uniform(90,98)
        elif distance <= 5 and "Rural" in cond:
            availability = np.random.uniform(99.95,100)
        elif "Pluie" in cond or "Brouillard" in cond or "Urbain" in cond:
            availability = np.random.uniform(99,99.95)
        else:
            availability = np.random.uniform(99.5,99.99)

        # Modulation adaptée
        if distance > 20 or "Pluie" in cond or "Brouillard" in cond or "Urbain" in cond:
            mod = np.random.choice(["BPSK","QPSK","8PSK","16-QAM"])
        else:
            mod = np.random.choice(self.modulations)

        # Classification liaison
        if rssi > -70 and snr >= 20 and ber <= 1e-6:
            status = "OK"
        elif rssi > -85 and snr >=10 and ber <= 1e-3:
            status = "Dégradé"
        else:
            status = "KO"

        return {
            "Condition": cond,
            "Distance_km": round(distance,2),
            "Frequency_GHz": freq,
            "Bandwidth_MHz": bw,
            "Modulation": mod,
            "TxPower_dBm": round(tx_power,2),
            "Gain_dBi": round(gain,2),
            "RSSI_dBm": round(rssi,2),
            "SNR_dB": round(snr,2),
            "BER": ber,
            "Availability_percent": round(availability,2),
            "Status": status
        }

    def generer_donnees(self, condition: str = None) -> pd.DataFrame:
        """
        Génère un DataFrame pour l'affichage CLI.
        """
        sample = self.simulate_fh()
        if condition:
            sample["Condition"] = condition
        df = pd.DataFrame([{
            "rssi": sample["RSSI_dBm"],
            "snr": sample["SNR_dB"],
            "ber": sample["BER"],
            "disponibilite": sample["Availability_percent"],
            "condition": sample["Condition"]
        }])
        return df

    def get_conditions_disponibles(self):
        return self.conditions


# --------------------------------------------------
# Test rapide CLI
# --------------------------------------------------
if __name__ == "__main__":
    sim = SimulateurFaisceauHertzien()
    for _ in range(5):
        sample = sim.simulate_fh()
        for k,v in sample.items():
            print(f"{k}: {v}")
        print("-"*40)
