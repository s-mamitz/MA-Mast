# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Aktualisiert bereits extrahierte Qualifikationspaare aus zuvor gespeicherten Daten.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 15:14:53 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Lese die Dateien ein
master_df = pd.read_csv('master_einheitlich.csv', sep=';', encoding='utf-8')
kombination_df = pd.read_csv('kombination_einheitlich.csv', sep=';', encoding='utf-8')

# Erstelle ein Dictionary für die Korrekturen
korrekturen = {}
for index, row in kombination_df.iterrows():
    original_pair = (row[0], row[1])
    corrected_pair = (row[3] if pd.notna(row[3]) else original_pair[0],
                      row[4] if pd.notna(row[4]) else original_pair[1])
    category = row[5]  # Kategorie aus Spalte 5
    
    korrekturen[original_pair] = (corrected_pair, category)  # Korrigiertes Paar und Kategorie

# Lege die Spaltenpaare für die Korrektur fest
spaltenpaare = [(30, 31), (32, 33), (34, 35), (36, 37), (38, 39), (40, 41), (42, 43)]

# Iteriere über alle Zeilen in master_df und korrigiere die Fehler
for index, row in master_df.iterrows():
    for spalte1, spalte2 in spaltenpaare:
        original_pair = (row[spalte1], row[spalte2])
        
        # Wenn das ursprüngliche Paar eine Korrektur hat, wende die Korrektur an
        if original_pair in korrekturen:
            corrected_pair, category = korrekturen[original_pair]
            master_df.iat[index, spalte1] = corrected_pair[0]  # Aktualisiere den Wert in Spalte 1
            master_df.iat[index, spalte2] = corrected_pair[1]  # Aktualisiere den Wert in Spalte 2

            # Füge die Kategorie in die neue Spalte ein
            new_column_index = master_df.shape[1]  # Aktueller Index für die neue Spalte
            # Überprüfe, ob die Kategorie-Spalte bereits existiert
            if f'Kategorie_{spalte1}_{spalte2}' not in master_df.columns:
                master_df.insert(new_column_index, f'Kategorie_{spalte1}_{spalte2}', category)  # Neue Spalte hinzufügen
            else:
                master_df.at[index, f'Kategorie_{spalte1}_{spalte2}'] = category  # Wert in existierender Spalte aktualisieren

# Ergebnisse speichern
master_df.to_csv('re_master_einheitlich.csv', sep=';', index=False, encoding='utf-8')

print("Die Korrekturen und neuen Daten wurden in 're_master_einheitlich.csv' gespeichert.")






