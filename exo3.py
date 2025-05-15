from itertools import combinations # generer tous les sous ensembles d'un ensemble
import numpy as np #calculs mathématiques
import pandas as pd # manipulation de dataframes
from pulp import * #programmation linéaire + optimisation linéaire
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from itertools import permutations
from cvxopt import matrix, solvers # quadratic programming
from matplotlib.ticker import FuncFormatter # POur les graphiques
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
 
 
# Question 1 -------------------------------------------------------

# Récupération des données de l'action de Google
data = pd.read_csv('/Users/sabine/Desktop/CYTech/S3/Optim_IA/Examen/GOOG.csv')

# Calcul des moyennes mobiles pour 20 et 40 jours
data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["SMA_40"] = data["Close"].rolling(window=40).mean()

# Affichage des moyennes mobiles
plt.figure(figsize=(14, 7))
plt.plot(data.index, data["Close"], label="Prix de clôture", color="blue")
plt.plot(data.index, data["SMA_20"], label="Moyenne mobile 20 jours", color="orange")
plt.plot(data.index, data["SMA_40"], label="Moyenne mobile 40 jours", color="purple")
plt.title("Moyennes mobiles pour l'action de Google")
plt.xlabel("Date")
plt.ylabel("Prix de clôture ($)")
plt.legend()
plt.show()

# Question 2 -------------------------------------------------------

# Création de la colonne de signaux d'achat/vente
data["Signal"] = 0  # Initialise la colonne à 0

# Remplissage de la colonne "Signal" en fonction des moyennes mobiles
for i in range(20, len(data)):
    if data["SMA_20"].iloc[i] > data["SMA_40"].iloc[i]:
        data.at[data.index[i], "Signal"] = 1
    else:
        data.at[data.index[i], "Signal"] = -1

# Création des DataFrames pour les signaux d'achat et de vente
buy_signals = data[data["Signal"] == 1]
sell_signals = data[data["Signal"] == -1]
 
# Graphique des prix de clôture et des signaux d'achat/vente
plt.figure(figsize=(14, 7))
plt.plot(data.index, data["Close"], label="Prix de clôture", color="blue")
plt.plot(data.index, data["SMA_20"], label="Moyenne mobile 20 jours", color="orange")
plt.plot(data.index, data["SMA_40"], label="Moyenne mobile 40 jours", color="purple")
 
# Ajout des signaux d'achat et de vente
plt.scatter(buy_signals.index, buy_signals["Close"], label="SMA_20 > SMA_40", marker="^", color="#8fbc8f", s=100)
plt.scatter(sell_signals.index, sell_signals["Close"], label="SMA_20 < SMA_40", marker="v", color="pink", s=100)
 
plt.title("Signaux d'achat et de vente basés sur les moyennes mobiles")
plt.xlabel("Date")
plt.ylabel("Prix de clôture ($)")
plt.legend()
plt.show()

# Evaluation de la stratégie -------------------------------------------------------

# Ajout de colonnes pour calculer les rendements
data["Position"] = data["Signal"].shift(1)  # Décalage pour prendre des décisions basées sur la journée précédente
data["Rendement"] = data["Close"].pct_change()  # Rendement quotidien

# Calcul des rendements de la stratégie
data["Rendement_strat"] = data["Position"] * data["Rendement"]

# Calcul de la performance cumulée
data["Rendement_total_strategie"] = (1 + data["Rendement_strat"]).cumprod()
data["Rendement_total_marche"] = (1 + data["Rendement"]).cumprod()


# Affichage de la performance
plt.figure(figsize=(14, 7))
plt.plot(data.index, data["Rendement_total_strategie"], label="Stratégie", color="green")
plt.plot(data.index, data["Rendement_total_marche"], label="Marché (Buy and Hold)", color="blue")
plt.title("Performance cumulée de la stratégie vs marché")
plt.xlabel("Date")
plt.ylabel("Performance cumulée")
plt.legend()
plt.show()

# Calcul du rendement de la stratégie
total_strategy_return = data["Rendement_total_strategie"].iloc[-1] - 1
total_market_return = data["Rendement_total_marche"].iloc[-1] - 1
print(f"Rendement total de la stratégie : {total_strategy_return:.2%}")
print(f"Rendement total du marché : {total_market_return:.2%}")


# Analyse des faux signaux

data["Rendement_strat"] = data["Position"] * data["Rendement"]
rendement_gagnant = len(data[data["Rendement_strat"] > 0])
rendement_perdant = len(data[data["Rendement_strat"] <= 0])

print(f"Nombre de trades gagnants : {rendement_gagnant}")
print(f"Nombre de trades perdants : {rendement_perdant}")
print(f"Taux de réussite : {rendement_gagnant / (rendement_gagnant + rendement_perdant):.2%}")