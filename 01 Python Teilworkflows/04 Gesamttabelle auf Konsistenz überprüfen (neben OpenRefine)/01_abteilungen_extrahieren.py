# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Extrahiert Abteilungsinformationen aus den Quelldaten und speichert diese in einer einheitlichen Tabelle.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 14:33:06 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Lesen der CSV-Datei mit der Titelzeile
df = pd.read_csv('ämter_einheitlich.csv', sep=';', header=0)

# Die Titelzeile speichern
header = df.columns.tolist()

# Nur die ersten 4 Ziffern in der 0. Spalte beibehalten
df.iloc[:, 0] = df.iloc[:, 0].astype(str).str[:4]

# Neue Tabelle erstellen, um Kombinationen zu sammeln
kombinationen = {}

# Durch jede Zeile iterieren
for _, row in df.iterrows():
    # Die Kombination der Werte in den Spalten 1 bis 4 als Schlüssel
    kombi_key = (row[header[1]], row[header[2]], row[header[3]], row[header[4]])
    
    # Wert aus der 0. Spalte
    wert_0 = row[header[0]]
    
    # Wenn die Kombination bereits existiert, den Wert hinzufügen
    if kombi_key in kombinationen:
        kombinationen[kombi_key].append(wert_0)
    else:
        # Neue Kombination mit dem ersten Wert aus der 0. Spalte erstellen
        kombinationen[kombi_key] = [wert_0]

# Ergebnis in ein DataFrame umwandeln
result = pd.DataFrame([
    [*key, ', '.join(values)] for key, values in kombinationen.items()
], columns=header[1:5] + [header[0]])

# Speichern der neuen Tabelle als CSV-Datei
result.to_csv('result_einheitlich.csv', sep=';', index=False)

# Erstellen der Tabellen mit eindeutigen Werten für jede Spalte (1-4)
for i in range(1, 5):
    unique_values = df[header[i]].drop_duplicates().sort_values().reset_index(drop=True)
    unique_df = pd.DataFrame(unique_values, columns=[header[i]])
    # Speichern der eindeutigen Werte als CSV-Datei
    unique_df.to_csv(f'unique_{header[i]}_einheitlich.csv', sep=';', index=False)

print("Die neuen Dateien 'result_einheitlich.csv' und 'unique_Spalte_einheitlich.csv' wurden erfolgreich erstellt.")
