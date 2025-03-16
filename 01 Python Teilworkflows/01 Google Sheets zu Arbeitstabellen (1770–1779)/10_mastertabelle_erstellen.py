# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:47:01 2024

@author: marcericmitzscherling
"""

import pandas as pd
import os

# Liste mit den Pfaden zu den CSV-Dateien
csv_pfade = [
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

# Eine Liste für DataFrames vorbereiten
dataframes = []

for dateipfad in csv_pfade:
    # Die CSV-Datei lesen
    df = pd.read_csv(dateipfad, sep=';')
    
    # DataFrame zur Liste hinzufügen
    dataframes.append(df)

# Eine Mastertabelle erstellen, indem alle DataFrames zusammengefügt werden
master_df = pd.concat(dataframes, ignore_index=True)

# Die Mastertabelle speichern
master_df.to_csv('master.csv', sep=';', index=False)

print("Die Verarbeitung der CSV-Dateien ist abgeschlossen.")