# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Fügt Hinweise wie "genannt" in vorhandene Namensdaten ein.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:13:47 2024

@author: marcericmitzscherling
"""

import pandas as pd

# CSV-Dateien einlesen
master_df = pd.read_csv('1 master_einheitlich.csv', sep=',')
namen_df = pd.read_csv('1 namen_einheitlich.csv', sep=',')

# Erstellen einer leeren Spalte in master_df für die kombinierten Werte aus namen_df
master_df['Namen_Info'] = ''

# Iteriere über die Zeilen von master_df und vergleiche die Namen in der ersten Spalte
for idx, row in master_df.iterrows():
    name = row[0]  # Name in der ersten Spalte von master_df
    
    # Filter die Zeile in namen_df, die denselben Namen enthält
    namen_row = namen_df[namen_df.iloc[:, 0] == name]
    
    # Wenn ein Treffer gefunden wurde, kombiniere die Werte in der Zeile von namen_df
    if not namen_row.empty:
        # Werte aus allen Spalten in namen_df, außer der ersten Spalte
        # Leere Werte (NaN) werden entfernt
        values = namen_row.iloc[0, 1:].dropna().astype(str).tolist()
        
        # Optional: Entferne leere Strings, falls vorhanden
        values = [v for v in values if v.strip() != '']
        
        # Kombiniere die verbleibenden Werte mit "|"
        combined_values = '|'.join(values)
        
        # Füge die kombinierten Werte in die neue Spalte "Namen_Info" in master_df ein
        master_df.at[idx, 'Namen_Info'] = combined_values

# Neue CSV-Datei speichern mit dem Präfix "namen_"
output_filename = '1_master_einheitlich.csv'
master_df.to_csv(output_filename, index=False, sep=',')
print(f"Datei '{output_filename}' wurde erfolgreich gespeichert.")
