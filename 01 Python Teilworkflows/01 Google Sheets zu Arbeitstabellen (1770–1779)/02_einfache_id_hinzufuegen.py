# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:30:20 2024

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
    # Den Dateinamen ohne 're_' und '.csv' extrahieren
    dateiname = os.path.basename(dateipfad)
    base_name = dateiname.replace('re_', '').replace('.csv', '')
    
    # Die CSV-Datei lesen
    df = pd.read_csv(dateipfad, sep=';')
    
    # Die erste Spalte (Index 0) mit den gewünschten Werten füllen
    df.iloc[:, 0] = [f'{base_name}-{i+1}' for i in range(len(df))]
    
    # Die bearbeitete Tabelle speichern (überschreibt die Originaldatei)
    df.to_csv(dateipfad, sep=';', index=False)
    
    # DataFrame zur Liste hinzufügen
    dataframes.append(df)

# Eine Mastertabelle erstellen, indem alle DataFrames zusammengefügt werden
#master_df = pd.concat(dataframes, ignore_index=True)

# Die Mastertabelle speichern
#master_df.to_csv('master.csv', sep=';', index=False)

print("Die Verarbeitung der CSV-Dateien ist abgeschlossen.")
