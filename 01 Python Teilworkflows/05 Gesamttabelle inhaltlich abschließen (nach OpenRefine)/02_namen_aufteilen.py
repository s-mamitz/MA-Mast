# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Teilt vollständige Namen in Vor- und Nachnamen auf.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:18:02 2024

@author: marcericmitzscherling
"""

import pandas as pd
import os

# Listen für Nachnamen zur Identifizierung
nachnamen_list = ["jun", "sen", "a Roda", "á Roda", "sen.", "jun.", "senior", "junior"]
nachnamen_list2 = ["Rheingraf", "Händel", "Galetti", "Trensch", "Treusch", "Löser", "Teuscher", "Teutscher", "Schertel", "Senf", "Senfft", "Senff", "Geyer", "Hochstedter", "Bachof"]

# Funktion zum Namen aufteilen
def split_name(name, max_first_names):
    if pd.isna(name):
        return [""] * (max_first_names + 1)  # Leere Felder für Vorname1 bis V5 und Nachname
    
    # Entferne alles nach ", (geb." oder einem "#" im Namen
    if ", (geb." in name:
        name = name.split(", (geb.")[0].strip()
    if "#" in name:
        name = name.split("#")[0].strip()
    if "senior" in name:
        name = name.split("senior")[0].strip()
    if "junior" in name:
        name = name.split("junior")[0].strip()
    
    parts = name.split()
    first_names = []
    last_name = ""
    
    i = 0
    while i < len(parts):
        part = parts[i]
        
        # Überprüfen, ob "N. N." als Ganzes behandelt werden muss
        if part == "N." and i + 1 < len(parts) and parts[i + 1] == "N.":
            first_names.append("N. N.")
            i += 2
            continue
        
        # Überprüfen, ob es sich um einen abgekürzten Vornamen handelt (Buchstabe gefolgt von einem Punkt)
        if len(part) == 2 and part[1] == '.':
            first_names.append(part)
        elif part in nachnamen_list or part in nachnamen_list2:
            last_name = " ".join(parts[i:])
            break
        elif len(part) > 3 or (i == 0):
            first_names.append(part)
        else:
            last_name = " ".join(parts[i:])
            break

        i += 1

    if not last_name and first_names:
        last_name = first_names.pop()

    while len(first_names) < max_first_names:
        first_names.append("")
    
    return first_names + [last_name.strip()]

# Funktion zur Verarbeitung mehrerer Dateien
def process_files(file_paths):
    for file_path in file_paths:
        df = pd.read_csv(file_path, delimiter=',')

        # Leeren der Spalten 17 und 20 bis 26
        df.iloc[:, [17] + list(range(20, 27))] = ""

        # Die Namen aus der 0. Spalte aufteilen
        max_first_names = 5
        split_names = df.iloc[:, 0].apply(split_name, max_first_names=max_first_names)

        # Die Spalten entsprechend aktualisieren
        for i in range(max_first_names):
            df.iloc[:, 20 + i] = [name[i] if i < len(name) else "" for name in split_names]
        
        # Adelspräposition in Spalte 17 identifizieren
        df['Adelspräposition'] = df.iloc[:, 0].apply(lambda x: 'von' if pd.notna(x) and ' von ' in f' {x} ' else ('zu' if pd.notna(x) and ' zu ' in f' {x} ' else ('de' if pd.notna(x) and ' de ' in f' {x} ' else "")))

        # Nachname in Spalte 25 speichern
        df.iloc[:, 25] = [name[max_first_names] for name in split_names]

        directory, original_filename = os.path.split(file_path)
        new_filename = f"namen_{original_filename}"  # Präfix "namen_" hinzufügen
        new_file_path = os.path.join(directory, new_filename)

        # DataFrame in die neue Datei speichern
        df.to_csv(new_file_path, sep=',', index=False)
        print(f"Datei '{new_file_path}' erfolgreich verarbeitet und gespeichert.")

file_paths = [
    'ma-mast_aktualisiert_einheitlich.csv'
]

process_files(file_paths)
