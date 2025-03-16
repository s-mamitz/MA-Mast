# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Ersetzt Q-IDs systematisch in den Datensätzen.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 18:56:58 2024

@author: marcericmitzscherling
"""

import pandas as pd

# CSV-Dateien einlesen
amt_neu_df = pd.read_csv('amt_neu_einheitlich.csv', header=None)  # Annahme: keine Header in amt_neu_einheitlich.csv
qid_amt_gesamt_df = pd.read_csv('qid-amt-gesamt_einheitlich.csv', header=None)  # Annahme: keine Header in qid-amt-gesamt_einheitlich.csv

# Erstelle ein Wörterbuch aus qid-amt-gesamt_einheitlich.csv für die Zuordnung
replace_dict = dict(zip(qid_amt_gesamt_df[0], qid_amt_gesamt_df[1]))

# Neue Datenstruktur für das Ergebnis
updated_amt_data = []

# Durchlaufe jede Zelle in amt_neu_einheitlich.csv und ersetze, falls möglich
for row in amt_neu_df.values:
    new_row = []
    for cell in row:
        # Nur ersetzen, wenn die Zelle nicht leer ist
        if pd.notna(cell) and cell in replace_dict:
            new_row.append(replace_dict[cell])  # Wert ersetzen
        else:
            new_row.append(cell)  # Originalwert beibehalten
            if pd.notna(cell) and cell not in replace_dict:
                print(f'Kommentar: Wert "{cell}" in amt_neu_einheitlich.csv wurde nicht in qid-amt-gesamt_einheitlich.csv gefunden.')
    updated_amt_data.append(new_row)

# Konvertiere das Ergebnis in ein DataFrame
updated_amt_neu_df = pd.DataFrame(updated_amt_data)

# Speichere die aktualisierte Tabelle mit dem Präfix "mitqid_"
updated_amt_neu_df.to_csv('mitqid_amt_neu_einheitlich.csv', index=False, header=False)

print('Die neue Datei mit dem Präfix "mitqid_" wurde erfolgreich gespeichert als mitqid_amt_neu_einheitlich.csv.')

