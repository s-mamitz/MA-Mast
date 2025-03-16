# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Fügt ein Feld hinzu, das dokumentiert, in welcher Quelle der Datensatz gelistet ist.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 09:19:38 2024

@author: marcericmitzscherling
"""

import csv
from collections import defaultdict

# Datei-Pfade für die Eingabe und Ausgabe
input_file = 'import.csv'
output_file = 'output.csv'

# Dictionary zur Speicherung der strukturierten Daten
data = defaultdict(lambda: defaultdict(set))

# Einlesen und Verarbeiten der CSV-Datei
with open(input_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # Header überspringen
    
    for row in reader:
        person_id = row[3]           # Person-ID aus Spalte 3
        document_id = row[83]        # Dokument-ID aus Spalte 83
        page_number = row[84]        # Seitenzahl aus Spalte 84
        
        # Seitenzahlen ohne Duplikate speichern
        data[person_id][document_id].add(page_number)

# Ausgabe in die neue CSV-Datei schreiben
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['person_id', 'document_id', 'pages'])  # Header schreiben
    
    # Daten strukturieren und schreiben
    for person_id, documents in data.items():
        for document_id, pages in documents.items():
            pages_sorted = sorted(pages, key=int)  # Seitenzahlen sortieren
            writer.writerow([person_id, document_id, ",".join(pages_sorted)])

print("Die Datei wurde erfolgreich erstellt und gespeichert als:", output_file)
