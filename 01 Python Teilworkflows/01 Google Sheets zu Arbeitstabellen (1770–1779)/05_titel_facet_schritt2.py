# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:30:58 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Funktionsdefinition
def update_original_tables(facet_table, file_paths):
    # Output-Tabelle einlesen
    output_df = pd.read_csv(facet_table, sep=';')

    # Jede Originaldatei einlesen und die Werte ersetzen
    for file_path in file_paths:
        df = pd.read_csv(file_path, sep=';')

        # Durch die Spalten der Output-Tabelle iterieren, um die Ersetzungen vorzunehmen
        for col in output_df.columns:
            if col.endswith('_new'):
                original_col = col.replace('_new', '')
                
                # Prüfen, ob die entsprechende Spalte in der Originaldatei vorhanden ist
                if original_col in df.columns:
                    # Iteriere über die Zeilen der Output-Tabelle
                    for index, row in output_df.iterrows():
                        new_value = row[col]
                        old_value = row[original_col]

                        # Falls die Zelle in der _new-Spalte nicht leer ist, wird ersetzt
                        if pd.notna(new_value) and new_value != '':
                            df[original_col] = df[original_col].replace(old_value, new_value)

        # Die aktualisierte Tabelle wieder speichern, gleiche Datei überschreiben
        df.to_csv(file_path, sep=';', index=False)
        print(f"Updated file saved as {file_path}")

# Beispiel für die Verwendung:
file_paths = [
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
facet_table = 'facet.csv'

update_original_tables(facet_table, file_paths)
