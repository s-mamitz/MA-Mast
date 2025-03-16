# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Gruppiert Amtseinträge und fügt Quellen hinzu.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:24:06 2024

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
            continue  # Falls kein gültes Jahr, überspringen wir diese Zeile
        
        # Berufe aus den relevanten Spalten
        professions = [row[i] for i in range(5, 24, 3) if row[i]]  # Berufe für das Jahr, hier auf Basis der Spezifikationen
        
        # Spezifizierungen aus den Spalten 25, 26, 27
        specifics = [row[25], row[26], row[27]]  # Wert aus Spalte 25, 26, 27
        
        # Amt und Berufe pro Person sammeln
        person_data[person_qid][office_qid].append((year, professions, specifics))

    # Bestimmen der maximalen Anzahl an Berufen pro Amtsgruppe
    max_professions_count = 0
    max_specifics_count = 0
    for offices in person_data.values():
        for records in offices.values():
            for _, professions, specifics in records:
                max_professions_count = max(max_professions_count, len(professions))
                max_specifics_count = max(max_specifics_count, len(specifics))

    # Header für die Ausgabedatei erstellen
    output_header = ["Person_QID", "Office_QID", "Start_Year", "Start_Year_us", "End_Year", "End_Year_us"]
    output_header.extend([f"Professions {i + 1}" for i in range(max_professions_count)])  # Dynamischer Header für Berufe

    # Header für Spezifizierungen, basierend auf der maximalen Anzahl an Zeilen in Amtsgruppen
    for i in range(max_specifics_count):
        output_header.extend([f"Wert 25 {i + 1}", f"Wert 26 {i + 1}", f"Wert 27 {i + 1}"])
        
    output_data.append(output_header)

    # Gruppierung pro Person und Amt
    for person_qid, offices in person_data.items():
        for office_qid, records in offices.items():
            # Sortiere nach Jahr und beginne Gruppenbildung
            records.sort()  # sortiert nach Jahr
            current_years = []
            current_professions = None
            current_specifics = []  # Liste für alle spezifischen Werte in der Amtsgruppe
            
            for year, professions, specifics in records:
                if current_professions is not None:
                    # Prüfen, ob die Berufe gleich sind und ob die Jahre kontinuierlich sind
                    if (set(professions) == set(current_professions) and 
                        year == current_years[-1] + 1):
                        current_years.append(year)  # Jahr zur aktuellen Gruppe hinzufügen
                        current_specifics.append(specifics)  # Spezifikationen hinzufügen
                    else:
                        # Wenn Berufe unterschiedlich oder Jahr nicht kontinuierlich, speichere die aktuelle Gruppe ab
                        start_year, end_year = current_years[0], current_years[-1]

                        output_data.append(create_output_row(person_qid, office_qid, start_year, end_year, current_professions, current_specifics, max_professions_count))
                        # Starte eine neue Gruppe
                        current_years = [year]
                        current_professions = professions
                        current_specifics = [specifics]  # Neue Liste mit aktuellen Spezifizierungen
                else:
                    # Erste Iteration: Initialisiere die erste Gruppe
                    current_years.append(year)
                    current_professions = professions
                    current_specifics = [specifics]  # Liste initialisieren

            # Füge die letzte Gruppe hinzu
            if current_years:
                start_year, end_year = current_years[0], current_years[-1]
                output_data.append(create_output_row(person_qid, office_qid, start_year, end_year, current_professions, current_specifics, max_professions_count))

    # Speichern der Ergebnisse in der neuen CSV
    with open(output_csv, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(output_data)

# Hilfsfunktion zur Erstellung der Zeilen für die neue CSV-Struktur
def create_output_row(person_qid, office_qid, start_year, end_year, professions, specifics, max_professions_count):
    row = [person_qid, office_qid]

    # Bestimmen, wo das Start- und Endjahr eingefügt werden soll
    start_year_us = start_year if start_year == 1768 else ''  # Nur 1768 geht in die US-Spalte
    end_year_us = end_year if end_year == 1779 else ''  # Nur 1779 geht in die US-Spalte
    
    row.append(start_year if start_year != 1768 else '')  # Normal Start Year oder leer
    row.append(start_year_us)  # Start Year US
    row.append(end_year if end_year != 1779 else '')  # Normal End Year oder leer
    row.append(end_year_us)  # End Year US

    # Berufe hinzufügen, füllen mit Leerzeichen, wenn weniger Berufe als Maximalanzahl vorhanden sind
    row.extend(professions + [''] * (max_professions_count - len(professions)))

    # Spezifizierungen hinzufügen, füllen mit Leerzeichen, wenn weniger Werte als maximal vorhanden sind
    max_specifics_count = len(specifics)
    for i in range(max_specifics_count):
        row.extend(specifics[i])  # Werte aus Wert 25, 26 und 27 hinzufügen
    for _ in range(max_specifics_count, 3):  # Wenn weniger Werte vorhanden sind, füllen wir mit Leerzeichen
        row.extend(['', '', ''])
        
    return row

# Ausführung des Skripts mit Beispiel-CSV-Dateinamen
input_csv = 'master.csv'  # Name der Eingabedatei
output_csv = 'output_data_pruef.csv'  # Name der Ausgabedatei
process_wiki_data(input_csv, output_csv)

