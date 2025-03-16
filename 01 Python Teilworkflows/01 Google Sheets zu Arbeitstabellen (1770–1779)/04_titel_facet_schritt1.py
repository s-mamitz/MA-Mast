# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 16:23:27 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Funktionsdefinition
def create_output_table(file_paths, facet_table):
    # DataFrame zur Sammlung aller Werte aus den Spalten 3-6
    combined_df = pd.DataFrame()

    for file_path in file_paths:
        # CSV-Datei einlesen
        df = pd.read_csv(file_path, sep=';')

        # Die Spalten 3-6 (0-index) extrahieren und zum kombinierten DataFrame hinzufügen
        combined_df = pd.concat([combined_df, df.iloc[:, 3:7]], ignore_index=True)

    # Für jede Spalte die einmaligen Werte extrahieren
    output_df = pd.DataFrame()
    for col in combined_df.columns:
        unique_values = combined_df[col].dropna().unique()
        unique_values = pd.Series(unique_values).sort_values().reset_index(drop=True)
        
        # Spaltenname aus der ersten Tabelle als Basis verwenden und neue Spalten erstellen
        col_name = col
        output_df[col_name] = unique_values
        output_df[f'{col_name}_new'] = ''

    # Ergebnis in eine neue CSV-Datei speichern
    output_df.to_csv(facet_table, sep=';', index=False)
    print(f"Output table saved as {facet_table}")


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

create_output_table(file_paths, facet_table)
