# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:18:02 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Aktualisierte Listen
adelstitel_list = ["Graf", "Gräfin", "Freiherr", "Freifrau", "Herzog", "Herzogin", "Fürst", "Fürstin"]
nachnamen_list = ["Heyduck", "jun"]
nachnamen_list2 = ["Rheingraf", "Händel", "Galetti", "Trensch", "Löser", "Teuscher", "Schertel"]

# Funktion zum Namen aufteilen
# Funktionsdefinition
def split_name(name, max_first_names):
    if pd.isna(name):
        return [""] * (max_first_names + 2)  # Leere Felder für Vorname1 bis V5, Nachname, genannt
    
    parts = name.split()
    first_names = []
    last_name = ""
    genannt_name = ""
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

    if ", genannt" in last_name:
        last_name, genannt_name = last_name.split(", genannt", 1)
    elif "genannt" in last_name:
        last_name, genannt_name = last_name.split("genannt", 1)
    
    last_name = last_name.strip()
    genannt_name = genannt_name.strip() if genannt_name else ""
    
    return first_names + [last_name, genannt_name]

# Funktion zur Verarbeitung mehrerer Dateien
# Funktionsdefinition
def process_files(file_paths):
    for file_path in file_paths:
        df = pd.read_csv(file_path, delimiter=';')
        
        # Die Namen aus der 9. Spalte aufteilen
        max_first_names = 5
        split_names = df.iloc[:, 9].apply(split_name, max_first_names=max_first_names)

        # Die Spalten entsprechend aktualisieren
        for i in range(max_first_names):
            df.iloc[:, 11 + i] = [name[i] if i < len(name) else "" for name in split_names]
            
        # Neue Spalte "Adelspräposition" einfügen
        df.insert(7, 'Adelspräposition', '')

        # Überprüfen auf Adelspräpositionen in Spalte 10 (0-index, also die 11. Spalte)
        df['Adelspräposition'] = df.iloc[:, 10].apply(lambda x: 'von' if pd.notna(x) and 'von' in x else "")
        
        df.iloc[:, 17] = [name[max_first_names] for name in split_names]  # Nachname in Spalte 16
        df.iloc[:, 18] = [name[max_first_names + 1] for name in split_names]  # Genannt in Spalte 17
        
        # Überschreiben der ursprünglichen Datei
        df.to_csv(file_path, sep=';', index=False)
        print(f"Datei '{file_path}' erfolgreich verarbeitet und gespeichert.")

# Beispiel für die Verwendung
file_paths = [
    #'re_1771.csv',
    #'re_1772.csv',
    #'re_1773.csv',
    #'re_1774.csv',
    #'re_1775.csv',
    #'re_1776.csv',
    #'re_1777.csv',
    #'re_1778.csv',
    #'re_1779.csv'
    're_master.csv'
]
process_files(file_paths)
