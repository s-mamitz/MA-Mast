# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Filtert Einträge, bei denen das Feld "Q1" leer ist.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 09:46:03 2024

@author: marcericmitzscherling
"""

import csv
import os
from collections import defaultdict

# Liste der Dateipfade zu den CSV-Dateien
file_paths = [
    're_1768_einheitlich.csv',
    're_1769_einheitlich.csv',
    're_1770_einheitlich.csv',
    're_1771_einheitlich.csv',
    're_1772_einheitlich.csv',
    're_1773_einheitlich.csv',
    're_1774_einheitlich.csv',
    're_1775_einheitlich.csv',
    're_1776_einheitlich.csv',
    're_1777_einheitlich.csv',
    're_1778_einheitlich.csv',
    're_1779_einheitlich.csv'
]

# Name der Datei, die qNachtrag und qNachtrag-Korrektur erhalten soll
nachtrag_file = 'qNachtrag_einheitlich.csv'
korrektur_file = 'qNachtrag-Korrektur_einheitlich.csv'

# Hilfsfunktion: Generiere eine eindeutige ID für Korrektureinträge
def generate_unique_id(counter):
    return f"KOR-{counter:04d}"

# Erstellen von qNachtrag und qNachtrag-Korrektur
nachtrag_entries = []
korrektur_entries = defaultdict(list)
unique_entry_ids = {}
korrektur_id_counter = 1

# Durchlaufe die CSV-Dateien in file_paths
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader)  # Kopfzeile
        
        # Durchlaufe jede Zeile und bearbeite Einträge, bei denen Spalte 30 leer ist
        for row in reader:
            id_value = row[0]
            etat = row[18]
            abt_1 = row[20]
            abt_2 = row[22]
            abt_3 = row[24]
            abt_4 = row[26]
            amt_q1 = None
            
            # Prüfe, ob Spalte 30 leer ist
            if not row[30]:
                # Iteriere durch Spalten 20, 22, 24, 26 um Amt-Q1 zu bestimmen
                for col in [20, 22, 24, 26]:
                    if row[col]:
                        amt_q1 = row[col]
                    else:
                        break

                # Füge den Eintrag zu qNachtrag hinzu
                nachtrag_entry = [id_value, etat, abt_1, abt_2, abt_3, abt_4, amt_q1]
                nachtrag_entries.append(nachtrag_entry)

                # Schlüssel für qNachtrag-Korrektur (ohne ID, aber mit den relevanten Spalten 1–5)
                korrektur_key = (etat, abt_1, abt_2, abt_3, abt_4)
                
                # Überprüfen, ob der Eintrag schon in qNachtrag-Korrektur existiert
                if korrektur_key not in unique_entry_ids:
                    # Generiere eine eindeutige ID für den Korrektureintrag
                    korrektur_id = generate_unique_id(korrektur_id_counter)
                    korrektur_id_counter += 1

                    # Füge den Eintrag zur Korrektur-Tabelle hinzu und speichere die ID
                    korrektur_entries[korrektur_key] = [etat, abt_1, abt_2, abt_3, abt_4, amt_q1, korrektur_id]
                    unique_entry_ids[korrektur_key] = korrektur_id
                else:
                    # Falls der Eintrag schon existiert, verwende die bestehende ID
                    korrektur_id = unique_entry_ids[korrektur_key]
                
                # Füge die Korrektur-ID dem Nachtragseintrag hinzu
                nachtrag_entry.append(korrektur_id)

# Schreiben der qNachtrag-Datei
print(f"Schreibe qNachtrag mit {len(nachtrag_entries)} Einträgen...")
with open(nachtrag_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # Kopfzeile für qNachtrag
    writer.writerow(['ID', 'Etat', 'Abt. 1', 'Abt. 2', 'Abt. 3', 'Abt. 4', 'Amt-Q1', 'Korrektur-ID'])
    # Schreibe alle Einträge in qNachtrag
    writer.writerows(nachtrag_entries)

# Schreiben der qNachtrag-Korrektur-Datei
print(f"Schreibe qNachtrag-Korrektur mit {len(korrektur_entries)} Einträgen...")
with open(korrektur_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # Kopfzeile für qNachtrag-Korrektur
    writer.writerow(['Etat', 'Abt. 1', 'Abt. 2', 'Abt. 3', 'Abt. 4', 'Amt-Q1', 'Korrektur-ID', 'Korrektur'])
    # Schreibe alle eindeutigen Einträge in qNachtrag-Korrektur
    for entry in korrektur_entries.values():
        writer.writerow(entry + [''])  # Füge die leere Korrektur-Spalte hinzu

print("Skript abgeschlossen.")
