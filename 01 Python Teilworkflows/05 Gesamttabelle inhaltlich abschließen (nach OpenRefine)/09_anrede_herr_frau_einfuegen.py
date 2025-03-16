# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Fügt Anreden ("Herr"/"Frau") systematisch in Datensätze ein.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 08:33:10 2024

@author: marcericmitzscherling
"""

import csv

# Datei-Pfade für die CSV-Dateien
master_file = '1_master_einheitlich.csv'
anrede_file = '2 anrede_einheitlich.csv'
output_file = '2_1_master_einheitlich.csv'

# Anrede-Daten lesen und als Wörterbuch speichern {ID: Wert in Spalte 2}
anrede_data = {}
with open(anrede_file, mode='r', newline='', encoding='utf-8') as anrede_csv:
    reader = csv.reader(anrede_csv, delimiter=',')
    for row in reader:
        id_anrede = row[1]  # ID aus Spalte 1 in anrede_einheitlich.csv
        value_anrede = row[2].strip()  # Wert aus Spalte 2 in anrede_einheitlich.csv (ohne führende/trailende Leerzeichen)
        
        # Nur nicht-leere Werte speichern
        if value_anrede:
            anrede_data[id_anrede] = value_anrede

# Verarbeiten der master CSV-Datei
with open(master_file, mode='r', newline='', encoding='utf-8') as master_csv, \
     open(output_file, mode='w', newline='', encoding='utf-8') as output_csv:
    
    reader = csv.reader(master_csv, delimiter=',')
    writer = csv.writer(output_csv, delimiter=',')
    
    # Variablen zur Speicherung der Werte und Datensätze
    dataset_values = set()
    current_id = None  # Aktueller Name/ID in Spalte 0
    
    rows = list(reader)  # Alle Zeilen im Speicher halten
    for i, row in enumerate(rows):
        
        # Prüfen, ob eine neue ID/Name in Spalte 0 vorhanden ist
        if row[0]:  
            # Falls `current_id` existiert, die gesammelten Werte in Spalte 69 eintragen
            if current_id is not None and dataset_values:
                # Zusammenfassen der Werte, Duplikate entfernen
                merged_values = '|'.join(sorted(dataset_values))
                rows[current_id][69] = merged_values  # Speichern in der ersten Zeile des Datensatzes
            
            # Neues Dataset beginnen
            current_id = i
            dataset_values = set()  # Zurücksetzen der Werte für das neue Dataset
        
        # Verarbeiten der aktuellen Zeile, falls die ID in `anrede_einheitlich.csv` gefunden wurde
        id_master = row[1]  # ID aus Spalte 1 in namen_master_einheitlich.csv
        if id_master in anrede_data:
            value_to_add = anrede_data[id_master].strip()  # Wert ohne führende/trailende Leerzeichen
            if value_to_add:  # Nur nicht-leere Werte berücksichtigen
                dataset_values.add(value_to_add)
        
        # Sicherstellen, dass nur die zusammengefassten Werte in der ersten Zeile des Datensatzes verbleiben
        row[69] = ''  # Löschen aller Werte in Spalte 69 in allen Zeilen

    # Den letzten Datensatz in `current_id` überprüfen und schreiben
    if current_id is not None and dataset_values:
        merged_values = '|'.join(sorted(dataset_values))  # Letzte Werte zusammenfassen
        rows[current_id][69] = merged_values
    
    # Alle Zeilen mit den aktualisierten Werten in die neue Datei schreiben
    writer.writerows(rows)

print("Die Datei wurde erfolgreich aktualisiert und unter anrede_namen_master_einheitlich.csv gespeichert.")

