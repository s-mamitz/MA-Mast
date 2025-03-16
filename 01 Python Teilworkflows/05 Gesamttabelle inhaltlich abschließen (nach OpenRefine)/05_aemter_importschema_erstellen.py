# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Erstellt ein Importschema für Amtseinträge.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:51:21 2024

@author: marcericmitzscherling
"""

import csv
from collections import defaultdict

# Eingabedatei und Ausgabedatei definieren
input_file = 'abteilungskombinationen_erweitert_einheitlich.csv'
output_file = 'output_einheitlich.csv'

# Dictionary für alle vorkommenden Werte aus Spalten 5–9 und deren zugehörige Werte aus Spalten 0–4
value_mapping = defaultdict(set)

# Lesen der Eingabedatei
with open(input_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    rows = list(reader)  # Alle Zeilen in einer Liste speichern

# Iteration von oben nach unten und von rechts nach links
for row in rows:
    for col_index in range(9, 4, -1):  # Spalten 9 bis 5
        cell_value = row[col_index]
        corresponding_value = row[col_index - 5]  # Wert in Spalten 0–4 (aktuelle Spalte -5)

        # Speichern des Zellwertes und zugehörigen Wertes, wenn der Zellwert nicht leer ist
        if cell_value:
            value_mapping[cell_value].add(corresponding_value)

# Filterung: Behalte nur Werte, die mindestens einmal vorkommen
filtered_value_mapping = {
    k: ' | '.join(f'"{v}"' for v in sorted(v))  # Jeder Wert wird im Code mit Anführungszeichen versehen
    for k, v in value_mapping.items() if len(v) > 0
}

# Schreiben der gefilterten Daten in die Ausgabedatei
with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Wert Spalte 5–9', 'Eindeutige zugehörige Werte Spalte 0–4'])

    # Schreiben der Werte und der zugehörigen, eindeutigen Werte (ohne Duplikate) in die Datei
    for unique_value, associated_values in filtered_value_mapping.items():
        writer.writerow([unique_value, associated_values])

print("Die Ausgabe wurde in 'output_einheitlich.csv' gespeichert.")