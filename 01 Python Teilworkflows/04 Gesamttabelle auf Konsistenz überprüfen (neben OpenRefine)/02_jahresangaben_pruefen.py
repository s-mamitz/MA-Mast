# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Prüft und validiert Jahresangaben in Datensätzen, korrigiert Fehler und speichert die validierten Ergebnisse.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 08:17:30 2024

@author: marcericmitzscherling
"""

import csv
from collections import defaultdict

def read_csv(file_path):
    """Liest die CSV-Datei ein und organisiert die Daten pro Person."""
    data = defaultdict(list)
    current_person = None

    # Lesen der CSV-Datei
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # Ignoriere leere Zeilen
            if not any(row):
                continue
            # Wenn die erste Spalte einen Namen enthält, setze diesen als aktuelle Person
            if row[0]:
                current_person = row[0]
            # Füge die Zeile der aktuellen Person hinzu, falls eine ID vorhanden ist
            if current_person and len(row) > 1 and row[1]:
                data[current_person].append(row[1])
    return data

def extract_years_from_ids(id_list):
    """Extrahiert die Jahreszahlen aus den IDs."""
    years = set()
    for id_val in id_list:
        try:
            # Extrahiere die ersten vier Ziffern als Jahr
            year = int(id_val[:4])
            years.add(year)
        except ValueError:
            # Falls die Konvertierung fehlschlägt, ignoriere diesen Eintrag
            continue
    return sorted(years)

def find_missing_years(years):
    """Findet Lücken in der Jahresliste, die kleiner oder gleich zwei Jahren sind."""
    missing_years = []
    for i in range(len(years) - 1):
        # Prüfe die Differenz zwischen aufeinanderfolgenden Jahren
        gap = years[i+1] - years[i]
        if gap > 2:
            # Füge die fehlenden Jahre zur Liste hinzu
            missing_years.extend(range(years[i] + 1, years[i+1]))
    return missing_years

def generate_report(data):
    """Erstellt den Bericht mit fehlenden Jahresangaben."""
    report = []
    for person, ids in data.items():
        # Extrahiere und sortiere die Jahreszahlen
        years = extract_years_from_ids(ids)
        # Finde die fehlenden Jahreszahlen
        missing_years = find_missing_years(years)
        if missing_years:
            # Erstelle einen neuen Berichtseintrag
            report.append([
                person,
                ",".join(ids),  # Alle gefundenen IDs, ,-separiert
                ",".join(map(str, missing_years))  # Fehlende Jahre, ,-separiert
            ])
    return report

def write_report(file_path, report):
    """Schreibt den Bericht in eine neue CSV-Datei."""
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        # Schreibe den Header
        writer.writerow(['Name', 'Gefundene IDs', 'Fehlende Jahre'])
        # Schreibe die Berichtsdaten
        writer.writerows(report)

def main():
    # Pfad zur Eingabedatei
    input_file = 'jahre_einheitlich.csv'
    # Pfad zur Ausgabedatei
    output_file = 'bericht_einheitlich.csv'

    # Lesen der Eingabedaten
    data = read_csv(input_file)
    # Generieren des Berichts
    report = generate_report(data)
    # Schreiben des Berichts in die Ausgabedatei
    write_report(output_file, report)

    print(f'Bericht wurde erfolgreich in {output_file} gespeichert.')

if __name__ == '__main__':
    main()
