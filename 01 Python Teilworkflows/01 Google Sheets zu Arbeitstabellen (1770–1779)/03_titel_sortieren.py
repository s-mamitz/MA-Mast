# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:02:51 2024

@author: marcericmitzscherling
"""

import pandas as pd
import re

# Funktionsdefinition
def process_table(df):

# Begriffe für akademische Grade und Adelstitel
    academic_titles = {
        'D.': 'Dr.',
        'D ': 'Dr.',
        'D,': 'Dr.',
        'Lic.': 'Lic.',
        'Lic ': 'Lic.',
        'M.': 'Magister',
        'M ': 'Magister'
    }
    noble_titles = [
        'Graf', 'Freiherr', 'Freyherr', 'Fürst', 'Prinz', 'Herzog', 'Freiin', 'Freyyn', 'Freyin'
    ]
    
    

    rules_col_3 = ['ll', 'x', 'Hoch']  # Bedingungen für Spalte 4 (Index 3)  
    rules_col_4 = ['.', 'gister', 'Lic', 'Mstr']         # Bedingungen für Spalte 5 (Index 4)
    rules_col_5 = ['Obrist', 'Leut', 'Maj', 'Mai', 'Haupt']
    rules_col_6_start = ['f', 'p', 'g', 'F', 'P', 'G']  # Bedingungen für Spalte 7 (Index 6) - nur am Anfang


    # Durchlaufe jede Zeile in den relevanten Spalten
    for index, row in df.iterrows():
        # Werte in Spalten 8 und 9 (Index 7 und 8) überprüfen
        for col in [7, 8]:
            value = row[col]
            if pd.notna(value) and isinstance(value, str):
                # Bereinige den Wert für die Kategorisierung
                value_clean = value.strip()

                if any(value_clean.startswith(cond) for cond in rules_col_6_start):
                    # Setze Wert in Spalte 7 (Index 6)
                    df.at[index, df.columns[6]] = value_clean
                    # Setze die Spalte, aus der der Wert stammt, auf None
                    df.at[index, df.columns[col]] = None
                elif any(cond in value_clean for cond in rules_col_3):
                    # Setze Wert in Spalte 4 (Index 3)
                    df.at[index, df.columns[3]] = value_clean
                    # Setze die Spalte, aus der der Wert stammt, auf None
                    df.at[index, df.columns[col]] = None
                elif any(cond in value_clean for cond in rules_col_4):
                    # Setze Wert in Spalte 5 (Index 4)
                    df.at[index, df.columns[4]] = value_clean
                    # Setze die Spalte, aus der der Wert stammt, auf None
                    df.at[index, df.columns[col]] = None
                elif any(cond in value_clean for cond in rules_col_5):
                    # Setze Wert in Spalte 4 (Index 3)
                    df.at[index, df.columns[5]] = value_clean
                    # Setze die Spalte, aus der der Wert stammt, auf None
                    df.at[index, df.columns[col]] = None
                # Belasse andere Werte in den ursprünglichen Spalten 8 oder 9
                else:
                    continue

       # Verarbeite Spalte 10 (Index 9)
        name = row[9]
        if pd.notna(name) and isinstance(name, str):
            name_clean = name.strip()
            
            # Entferne "Heyduck" und setze "Heiduck" in Spalte 21 (Index 20)
            if "Heyduck" in name_clean:
                name_clean = name_clean.replace("Heyduck", "").strip()
                df.at[index, df.columns[20]] = "Heiduck"

            # Verarbeite akademische Grade
            for prefix, degree in academic_titles.items():
                if name_clean.startswith(prefix):
                    df.at[index, df.columns[4]] = degree  # Setze akademischen Grad in Spalte 5 (Index 4)
                    name_clean = name_clean[len(prefix):].strip()  # Entferne Präfix

            # Verarbeite Adelstitel
            titles_found = [title for title in noble_titles if title in name_clean]
            if titles_found:
                # Setze den Adelstitel in Spalte 7 (Index 6)
                df.at[index, df.columns[6]] = ' '.join(titles_found)
                # Entferne Adelstitel aus dem Namen
                for title in titles_found:
                    name_clean = name_clean.replace(title, '').strip()

            # Entferne führende Zeichen vor dem ersten Buchstaben, wenn der Name mit „ .“ beginnt
            if name_clean.startswith(' .'):
                name_clean = name_clean.lstrip(' .').lstrip()
            
            #Entfernen doppelte Leerzeichen
            name_clean = re.sub(r'\s+', ' ', name_clean)
            name_clean = name_clean.strip()

            # Setze den bereinigten Namen in Spalte 10 (Index 9) zurück
            df.at[index, df.columns[9]] = name_clean

# Liste der Pfade zu den CSV-Dateien
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

# Verarbeite jede Datei in der Liste
for file_path in file_paths:
    # Lese die CSV-Datei mit ; als Trennzeichen
    df = pd.read_csv(file_path, delimiter=';')
    
    # Überprüfe die Dimensionen der geladenen DataFrame
    print(f"Verarbeite Datei: {file_path}")

    # Verarbeite die Tabelle
    try:
        process_table(df)
    except ValueError as e:
        print(f"Fehler bei der Verarbeitung der Datei {file_path}: {e}")
        continue
    
    # Speichere die bearbeitete CSV-Datei
    df.to_csv(file_path, sep=';', index=False)
    print(f"Datei erfolgreich gespeichert: {file_path}")
