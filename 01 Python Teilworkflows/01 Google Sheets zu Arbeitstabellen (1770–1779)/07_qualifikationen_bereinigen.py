# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 13:13:19 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Pfade zu den CSV-Dateien hier eingeben
csv_paths = [
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

# Funktionsdefinition
def process_csv(file_path):
    # Lade die CSV-Datei
    df = pd.read_csv(file_path, sep=';')
    
    # Schritt 1: Lösche alle Spalten ab Spalte 21, deren Titel "Spez" enthalten
    start_col = 21
    # Filtere die Spalten, die "Spez" im Titel haben
    columns_to_keep = [col for col in df.columns[start_col:] if 'Spez' not in col]
    df_filtered = df.iloc[:, :start_col].join(df[columns_to_keep])
    
    # Schritt 2: Extrahiere alle nicht-leeren Werte ab Spalte 21
    values = []
    for _, row in df_filtered.iterrows():
        non_empty_values = row[start_col:].dropna().tolist()
        values.append(non_empty_values)
    
    # Schritt 3: Teile Werte mit "und" auf
    split_values = []
    for row_values in values:
        new_row = []
        for value in row_values:
            # Teile sowohl nach "und " als auch nach ", " auf
            parts = [part.strip() for part in value.split("und ")]
            final_parts = []
            for part in parts:
                # Teile weiter nach ", "
                final_parts.extend(part.split(", "))
            new_row.extend(final_parts)
        split_values.append(new_row)
    
    # Schritt 4: Bestimme die maximale Anzahl von Werten pro Zeile
    max_cols = max(len(row) for row in split_values)
    
    # Schritt 5: Lösche alle Spalten ab und inklusive Spalte 21
    df_result = df_filtered.iloc[:, :start_col]
    
    # Füge neue Spalten hinzu: Q1, Q2, ..., Qmax
    for i in range(max_cols):
        df_result[f'Q{i+1}'] = pd.NA
    
    # Füge die "Spez"-Spalten hinzu: Q1 Spez, Q2 Spez, ..., Qmax Spez
    for i in range(max_cols):
        df_result.insert(start_col + 2*i + 1, f'Q{i+1} Spez', pd.NA)
    
    # Schritt 6: Trage die Werte in die neuen Spalten ein
    for i, row_values in enumerate(split_values):
        for j, value in enumerate(row_values):
            if j < max_cols:
                df_result.iloc[i, start_col + 2*j] = value
    
    # Speichere die bearbeitete Tabelle zurück in die CSV-Datei
    df_result.to_csv(file_path, sep=';', index=False)

# Verarbeite alle CSV-Dateien
for path in csv_paths:
    process_csv(path)
