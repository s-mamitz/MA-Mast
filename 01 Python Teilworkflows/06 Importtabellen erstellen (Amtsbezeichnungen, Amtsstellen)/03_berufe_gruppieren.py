# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Gruppiert Berufseinträge übersichtlich.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 19:27:07 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Schritt 1: Daten einlesen
df = pd.read_csv('master_beruf.csv', sep=',', header=0)

# Schritt 2: Datenstruktur für Ergebnisse
results = {}

# Schritt 3: Gruppierung nach Person (ID)
for _, row in df.iterrows():
    person_id = row[3]  # Spalte 3, Person-ID
    amt = row[4]        # Spalte 4, Amt
    jahr = int(row[2])  # Spalte 2, Jahr (in Ganzzahl konvertieren)
    
    # Berufsgruppen: 4er-Gruppen
    beruf_group = []
    for i in range(5, 33, 4):  # Von Spalte 5 bis 32 in Schritten von 4
        beruf_info = row[i:i+4].fillna('').astype(str).tolist()
        beruf_group.append(beruf_info)  # Füge die Gruppe hinzu

    # Eindeutige Berufe, deren Ämter und Jahre sammeln
    for beruf in beruf_group:
        if any(b.strip() for b in beruf):  
            beruf_tuple = tuple(beruf)  # Konvertiere zur Tuple, um die Spalten klar zu definieren
            if (person_id, beruf_tuple) not in results:
                results[(person_id, beruf_tuple)] = {'ämter': set(), 'jahre': set()}
            results[(person_id, beruf_tuple)]['ämter'].add(amt)
            results[(person_id, beruf_tuple)]['jahre'].add(jahr)

# Schritt 4: Ergebnisse speichern
output_data = []
for (person_id, beruf), value in results.items():
    # Ämter zu einer kommaseparierten Liste umwandeln
    amt_list = ', '.join(sorted(value['ämter']))  # Ämter als kommaseparierte Liste
    jahr_list = sorted(value['jahre'])  # Sortiere Jahre

    # Jahreszeitraum in lückenlose Segmente aufteilen
    split_jahre = []
    current_segment = [jahr_list[0]]

    for i in range(1, len(jahr_list)):
        if jahr_list[i] == jahr_list[i - 1] + 1:
            # Jahr gehört zum aktuellen Segment
            current_segment.append(jahr_list[i])
        else:
            # Segment beenden und zum nächsten starten
            split_jahre.append(current_segment)
            current_segment = [jahr_list[i]]
    
    # Füge das letzte Segment hinzu
    split_jahre.append(current_segment)

    # Füge für jedes Segment eine Zeile hinzu mit Beginn- und Endjahr
    for segment in split_jahre:
        # Beginn- und Endjahr des Segments
        beginn_jahr = segment[0]
        end_jahr = segment[-1]

        # Prüfen, ob das Beginn- oder Endjahr speziell ist (1768 bzw. 1779)
        beginn_jahr_us = beginn_jahr if beginn_jahr == 1768 else ''
        end_jahr_us = end_jahr if end_jahr == 1779 else ''
        
        # Standardmäßig die Jahre in die Beginn- und Endjahr-Spalten
        output_data.append([
            person_id,
            *list(beruf),
            amt_list,
            beginn_jahr if beginn_jahr != 1768 else '',
            end_jahr if end_jahr != 1779 else '',
            beginn_jahr_us,  # Beginnjahr us wird nur gesetzt, wenn es 1768 ist
            end_jahr_us      # Endjahr us wird nur gesetzt, wenn es 1779 ist
        ])

# Erstellen des DataFrames
columns = ['Person_ID', 'Beruf_1', 'Beruf_2', 'Beruf_3', 'Beruf_4', 'Ämter', 'Beginnjahr', 'Endjahr', 'Beginnjahr us', 'Endjahr us']  # Neue Spalten für Beginn- und Endjahr us

output_df = pd.DataFrame(output_data, columns=columns)
output_df.to_csv('berufe_uebersicht.csv', index=False, sep=',')

