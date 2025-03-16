# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Gruppiert Amtseinträge zur übersichtlichen Auswertung.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:33:40 2024

@author: marcericmitzscherling
"""

import csv
from collections import defaultdict

# Funktion zur Gruppierung und Bearbeitung der CSV-Daten
def process_wiki_data(input_csv, output_csv):
    # Daten aus CSV einlesen und sortieren
    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Überspringe den Header der Eingabedatei
        header = next(reader)
        
        # Lade die restlichen Daten
        data = list(reader)
    
    # Die Daten nach Q-ID der Person (Spalte 4) sortieren
    data.sort(key=lambda x: (x[4], int(x[2])))  # Nach Person und Jahr sortieren

    # Ergebnisliste für den neuen CSV-Inhalt
    output_data = []
    
    # Dictionary zur Speicherung aller Daten pro Person und Amt
    person_data = defaultdict(lambda: defaultdict(list))
    
    # Daten verarbeiten und gruppieren
    for row in data:
        person_qid = row[3]  # Q-ID der Person
        office_qid = row[4]  # Amt-QID
        
        try:
            year = int(row[2])   # Jahr der Anstellung (umwandeln in int)
        except ValueError:
            continue  # Falls kein gültiges Jahr, überspringen wir diese Zeile
        
        # Berufe aus den relevanten Spalten
        professions = [row[i] for i in range(5, 24, 3) if row[i]]  # Berufe für das Jahr, hier auf Basis der Spezifikationen
        
        # Amt und Berufe pro Person sammeln
        person_data[person_qid][office_qid].append((year, professions))

    # Bestimmen der maximalen Anzahl an Berufen pro Amtsgruppe
    max_professions_count = 0
    for offices in person_data.values():
        for records in offices.values():
            for _, professions in records:
                max_professions_count = max(max_professions_count, len(professions))

    # Header für die Ausgabedatei erstellen
    output_header = ["Person_QID", "Office_QID", "Start_Year", "End_Year"]
    output_header.extend([f"Professions {i + 1}" for i in range(max_professions_count)])  # Dynamischer Header für Berufe
    output_data.append(output_header)

    # Gruppierung pro Person und Amt
    for person_qid, offices in person_data.items():
        for office_qid, records in offices.items():
            # Sortiere nach Jahr und beginne Gruppenbildung
            records.sort()  # sortiert nach Jahr
            current_years = []
            current_professions = None
            
            for year, professions in records:
                if current_professions is not None:
                    # Prüfen, ob die Berufe gleich sind und ob die Jahre kontinuierlich sind
                    if set(professions) == set(current_professions) and year == current_years[-1] + 1:
                        current_years.append(year)  # Jahr zur aktuellen Gruppe hinzufügen
                    else:
                        # Wenn Berufe unterschiedlich oder Jahr nicht kontinuierlich, speichere die aktuelle Gruppe ab
                        start_year, end_year = current_years[0], current_years[-1]
                        output_data.append(create_output_row(person_qid, office_qid, start_year, end_year, current_professions, max_professions_count))
                        # Starte eine neue Gruppe
                        current_years = [year]
                        current_professions = professions
                else:
                    # Erste Iteration: Initialisiere die erste Gruppe
                    current_years.append(year)
                    current_professions = professions

            # Füge die letzte Gruppe hinzu
            if current_years:
                start_year, end_year = current_years[0], current_years[-1]
                output_data.append(create_output_row(person_qid, office_qid, start_year, end_year, current_professions, max_professions_count))

    # Speichern der Ergebnisse in der neuen CSV
    with open(output_csv, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output_data)

# Hilfsfunktion zur Erstellung der Zeilen für die neue CSV-Struktur
def create_output_row(person_qid, office_qid, start_year, end_year, professions, max_professions_count):
    row = [person_qid, office_qid, start_year, end_year]
    # Berufe hinzufügen, füllen mit Leerzeichen, wenn weniger Berufe als Maximalanzahl vorhanden sind
    row.extend(professions + [''] * (max_professions_count - len(professions)))
    return row

# Ausführung des Skripts mit Beispiel-CSV-Dateinamen
input_csv = 'master.csv'  # Name der Eingabedatei
output_csv = 'output_data.csv'  # Name der Ausgabedatei
process_wiki_data(input_csv, output_csv)




