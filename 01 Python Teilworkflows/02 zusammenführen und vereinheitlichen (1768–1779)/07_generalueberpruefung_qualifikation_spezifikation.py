# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Qualifikationen und Spezifikationen allgemein überprüfen

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 15:02:28 2024

@author: marcericmitzscherling
"""

import pandas as pd
from collections import defaultdict

# Definiere die Pfade zu den CSV-Dateien
file_paths = [
    're_1768.csv',
    're_1769.csv',
    're_1770.csv',
    're_1771.csv',
    're_1772.csv',
    're_1773.csv',
    're_1774.csv',
    're_1775.csv',
    're_1776.csv',
    're_1777.csv',
    're_1778.csv',
    're_1779.csv'
]

# Lade alle CSV-Dateien in einen gemeinsamen DataFrame
df_list = [pd.read_csv(file, sep=';', header=0) for file in file_paths]
combined_df = pd.concat(df_list, ignore_index=True)

# Definiere die Spaltenpaare
spaltenpaare = [(30, 31), (32, 33), (34, 35), (36, 37), (38, 39), (40, 41), (42, 43)]

# Initialisiere ein Dictionary für die Zählung der Kombinationen
kombinationen = defaultdict(int)

# Iteriere über jedes Spaltenpaar
for spalte1, spalte2 in spaltenpaare:
    # Extrahiere die relevanten Spalten
    pairs = combined_df[[combined_df.columns[spalte1], combined_df.columns[spalte2]]]
    
    # Iteriere über jede Zeile und zähle die Kombinationen
    for index, row in pairs.iterrows():
        # Erstelle einen Schlüssel aus den beiden Spalten
        key = (row.iloc[0], row.iloc[1])  # Tuple mit den Werten
        kombinationen[key] += 1  # Erhöhe den Zähler für diese Kombination

# Erstelle eine Liste der Ergebnisse
results = []
for (q, spez), count in kombinationen.items():
    results.append([q, spez, count, '', ''])  # Füge zwei leere Spalten hinzu

# Erstelle ein DataFrame aus den Ergebnissen
results_df = pd.DataFrame(results, columns=['Q', 'Spez', 'Anzahl', 'QNeu', 'SpezNeu'])

# Speichere das Ergebnis in einer CSV-Datei
results_df.to_csv('kombinationen.csv', sep=';', index=False)

print("Die Kombinationen wurden erfolgreich in 'kombinationen.csv' gespeichert.")
