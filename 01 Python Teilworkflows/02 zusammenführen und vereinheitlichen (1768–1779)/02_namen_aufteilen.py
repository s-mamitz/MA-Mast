# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Namen in Vor- und Nachname aufteilen

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:18:02 2024

@author: marcericmitzscherling
"""

import pandas as pd
import os

# Aktualisierte Listen
adelstitel_list = ["Freiherr", "Freifrau", "Herzog", "Herzogin", "Fürst", "Fürstin", "Edler"]
nachnamen_list = ["jun", "sen", "a Roda", "á Roda", "sen.", "jun."]
nachnamen_list2 = ["Rheingraf", "Händel", "Galetti", "Trensch", "Treusch", "Löser", "Teuscher", "Teutscher", "Schertel", "Senf", "Senfft", "Senff", "Geyer", "Hochstedter", "Bachof"]

# Funktion zum Namen aufteilen
def split_name(name, max_first_names):
    if pd.isna(name):
        return [""] * (max_first_names + 2)  # Leere Felder für Vorname1 bis V5, Nachname, genannt
    
    # Schritt 1: Extrahiere den "genannt"-Teil
    genannt_name = ""
    if ", genannt" in name:
        name, genannt_name = name.split(", genannt", 1)
    elif "genannt" in name:
        name, genannt_name = name.split("genannt", 1)

    # Entferne überflüssige Leerzeichen
    name = name.strip()
    genannt_name = genannt_name.strip() if genannt_name else ""

    parts = name.split()
    first_names = []
    last_name = ""
    adelstitel = ""

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
        elif part in adelstitel_list:
            adelstitel = part
        elif part in nachnamen_list:
            last_name = " ".join(parts[i:])
            if first_names:
                last_name = " ".join(parts[len(first_names) - 1:i]) + " " + last_name
            else:
                last_name = " ".join(parts[:i]) + " " + last_name
            break
        elif part in nachnamen_list2:
            last_name = " ".join(parts[i:])
            break
        elif len(part) > 3 or (i == 0):
            first_names.append(part)
        else:
            last_name = " ".join(parts[i:])
            break

        i += 1

    if not last_name:
        if first_names:
            last_name = first_names.pop()

    while len(first_names) < max_first_names:
        first_names.append("")

    last_name = last_name.strip()
    
    return first_names + [last_name, genannt_name]

# Funktion zur Verarbeitung mehrerer Dateien
def process_files(file_paths):
    for file_path in file_paths:
        df = pd.read_csv(file_path, delimiter=';')
        
        # Die Namen aus der 9. Spalte aufteilen
        max_first_names = 5
        split_names = df.iloc[:, 9].apply(split_name, max_first_names=max_first_names)

        # Die Spalten entsprechend aktualisieren
        for i in range(max_first_names):
            df.iloc[:, 11 + i] = [name[i] if i < len(name) else "" for name in split_names]
            

        # Überprüfen auf Adelspräpositionen in Spalte 9
        df['Adelspräposition'] = df.iloc[:, 9].apply(lambda x: 'von' if pd.notna(x) and f' von ' in f' {x} ' else ('zu' if pd.notna(x) and f' zu ' in f' {x} ' else ('de' if pd.notna(x) and f' de ' in f' {x} ' else "")))

        
        df.iloc[:, 16] = [name[max_first_names] for name in split_names]  # Nachname in Spalte 16
        df.iloc[:, 17] = [name[max_first_names + 1] for name in split_names]  # Genannt in Spalte 17
        
        directory, original_filename = os.path.split(file_path)
        #new_filename = f"re_{original_filename}"
        new_filename = f"{original_filename}"
        new_file_path = os.path.join(directory, new_filename)
    
        # DataFrame in die neue Datei speichern
        df.to_csv(new_file_path, sep=';', index=False)
        print(f"Datei '{new_file_path}' erfolgreich verarbeitet und gespeichert.")

# Beispiel für die Verwendung
# file_paths = [
#     '1768.csv',
#     '1769.csv',
#     '1770.csv',
#     '1771.csv',
#     '1772.csv',
#     '1773.csv',
#     '1774.csv',
#     '1775.csv',
#     '1776.csv',
#     '1777.csv',
#     '1778.csv',
#     '1779.csv'
# ]

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

process_files(file_paths)
