# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:34:50 2024

@author: marcericmitzscherling
"""

import pandas as pd
import os

# Liste der Pfade zu den Tabellen (CSV-Dateien)
table_paths = [
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

# Liste der Stopwörter
stopwords = ["des ", "zu ", "zur ", "wegen der ", "bei dem ", "bey dem ", "bei der ", "bey der ", "auf ", "der ", "bey ", "bei ", ]

# Liste der unerwünschten Buchstabenkombinationen
unwanted_words = ["Her", "Pferd"]

# Funktion, die eine Zelle bearbeitet und das Trennen durchführt
# Funktionsdefinition
def process_cell(cell_value, stopwords, unwanted_words):
    if pd.isna(cell_value):  # Wenn die Zelle leer ist, keine Bearbeitung
        return cell_value, None
    
    for stopword in stopwords:
        if stopword in cell_value:
            # Splitten an der Stelle des Stopworts
            split_value = cell_value.split(stopword, 1)
            remainder = split_value[1] if len(split_value) > 1 else ""
            next_word = remainder.split()[0] if remainder else ""

            # Prüfen, ob das nächste Wort nicht in der Liste unwanted_words ist
            if not any(remainder.startswith(uw) for uw in unwanted_words):
                # Rückgabe des angepassten Werts und der verschobenen Ortsinformation
                return split_value[0].strip(), remainder.strip()
    
    # Wenn kein Stopwort gefunden oder unwanted_word erkannt wird, bleibt der Wert unverändert
    return cell_value, None

# Hauptverarbeitung für jede Tabelle
for table_path in table_paths:
    # Einlesen der Tabelle
    df = pd.read_csv(table_path, delimiter=';')

    # Bestimmen der Gesamtanzahl der Spalten in der Tabelle
    total_columns = len(df.columns)

    # Durchlaufen jeder zweiten Spalte ab der 21. Spalte (Index 20)
    for col in range(21, total_columns - 1, 2):  # Verarbeiten jeder zweiten Spalte und der direkt daneben
        for index, row in df.iterrows():
            cell_value = row[col]  # Aktueller Wert in der Spalte

            # Zelleninhalt verarbeiten
            new_value, moved_value = process_cell(cell_value, stopwords, unwanted_words)

            # Aktualisieren der Zellen, wenn eine Änderung erfolgt
            df.at[index, df.columns[col]] = new_value  # Originalwert aktualisieren
            if moved_value:  # Falls etwas verschoben werden soll
                df.at[index, df.columns[col + 1]] = moved_value

    # Speichern der Tabelle mit dem neuen Namen (alter Name + "s")
    new_table_path = os.path.splitext(table_path)[0] + '.csv'
    df.to_csv(new_table_path, sep=';', index=False)

print("Alle Tabellen wurden erfolgreich verarbeitet und als neue Dateien gespeichert.")
