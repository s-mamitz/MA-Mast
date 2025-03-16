# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Fehlende Q1-Werte systematisch auffüllen

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 12:28:42 2024

@author: marcericmitzscherling
"""

import pandas as pd

def load_csv_files(file_paths):
    """Lade CSV-Dateien aus einer Liste von Dateipfaden und drucke die Spalten."""
    csv_files = {}
    for file_path in file_paths:
        file_name = file_path.split('/')[-1]  # Extrahiere den Dateinamen
        table_id = file_name.split('_')[1].split('.')[0]  # 1768 aus re_1768.csv
        csv_files[table_id] = pd.read_csv(file_path, sep=';')
        print(f"Tabelle {table_id} hat die Spalten: {csv_files[table_id].columns.tolist()}")  # Debugging: Spalten anzeigen
    return csv_files

def find_empty_column(row, start_col, step=2):
    """Finde die nächste leere Spalte in einem bestimmten Schritt."""
    for col in range(start_col, start_col + step * 3, step):
        if pd.isna(row[col]):
            return col
    return None

def process_entries(qNachtrag, qNachtrag_korrektur, csv_files):
    """Prozessiere die Einträge von qNachtrag und qNachtrag-Korrektur."""
    for _, row_nachtrag in qNachtrag.iterrows():
        # Extrahiere die ID's
        first_id = row_nachtrag['ID']  # Spalte 'ID' in qNachtrag
        second_id = row_nachtrag['Korrektur-ID']  # Spalte 'Korrektur-ID' in qNachtrag
        
        # Finde die zugehörige Zeile in qNachtrag-Korrektur über die Spalte 'Korrektur-ID'
        match_korrektur = qNachtrag_korrektur[qNachtrag_korrektur['Korrektur-ID'] == second_id]
        if match_korrektur.empty:
            print(f"Keine Übereinstimmung für die ID {second_id} in qNachtrag-Korrektur gefunden.")
            continue
        
        # Hole die relevanten Daten aus qNachtrag-Korrektur
        values_to_insert = match_korrektur.iloc[0][['Q1', 'Q1 Spez', 'Q2', 'Q2 Spez']].values
        
        # Verarbeite die erste ID, um die Datei zu finden
        table_id, entry_id = first_id.split('-')
        
        if table_id not in csv_files:
            print(f"Tabelle {table_id} nicht gefunden.")
            continue
        
        # Finde den zu bearbeitenden Eintrag in der Tabelle
        table = csv_files[table_id]
        entry_row = table[table['ID'] == first_id]  # Angenommen, die ID steht in der Spalte 'ID'
        
        if entry_row.empty:
            print(f"Eintrag {first_id} nicht in Tabelle {table_id} gefunden.")
            continue
        
        # Debugging: Ausgabe der Spalten, um sicherzustellen, dass die Spalten 30 bis 33 vorhanden sind
        print(f"Eintrag gefunden: {entry_row.iloc[0].to_dict()}")
        
        # Füge die Werte in die entsprechenden Spalten (30–33) ein
        for i, value in enumerate(values_to_insert):
            if pd.notna(value):  # Nur wenn der Wert nicht leer ist
                empty_col = find_empty_column(entry_row.iloc[0], 30 + i, step=2)
                if empty_col is not None:
                    table.at[entry_row.index[0], table.columns[empty_col]] = value  # Verwende den Spaltennamen
                else:
                    print(f"Keine freien Spalten für Wert {value} in Tabelle {table_id}, Eintrag {first_id} gefunden.")

    # Speichern der bearbeiteten Tabellen
    for table_id, table in csv_files.items():
        file_path = f"re_{table_id}.csv"
        table.to_csv(file_path, sep=';', index=False)
        print(f"Tabelle {table_id} wurde erfolgreich in {file_path} gespeichert.")

# Hauptskript-Logik
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
qNachtrag_path = 'qNachtrag.csv'
qNachtrag_korrektur_path = 'qNachtrag-Korrektur.csv'

# Lade die qNachtrag und qNachtrag-Korrektur Tabellen
qNachtrag = pd.read_csv(qNachtrag_path, sep=';')
qNachtrag_korrektur = pd.read_csv(qNachtrag_korrektur_path, sep=';')

# Lade alle relevanten CSV-Dateien aus der Liste von Dateipfaden
csv_files = load_csv_files(file_paths)

# Prozessiere die Einträge und bearbeite die CSV-Dateien
process_entries(qNachtrag, qNachtrag_korrektur, csv_files)
