# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Aktualisiert Amtseinträge nebenstehend in der Tabelle.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:13:43 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Definieren der Dateipfade
mast_path = 'namen_ma-mast_aktualisiert_einheitlich.csv'
amt_path = 'abteilungskombinationen_erweitert_einheitlich.csv'
output_path = 'amt_namen_ma-mast_aktualisiert_einheitlich.csv'

# Einlesen der CSV-Dateien
mast_df = pd.read_csv(mast_path, sep=',')
amt_df = pd.read_csv(amt_path, sep=',')

# Definieren der relevanten Spaltenindizes
mast_columns = [27, 29, 31, 33, 35]  # Spalten für Kombinationen in mast_einheitlich.csv
amt_columns = [0, 1, 2, 3, 4]        # Spalten für Kombinationen in amt_einheitlich.csv
amt_values_columns = [5, 6, 7, 8, 9] # Spalten für Werte in amt_einheitlich.csv

# Erstellen eines Dictionarys für schnellen Zugriff auf die Werte in amt_einheitlich.csv
amt_dict = {}
for _, row in amt_df.iterrows():
    key = tuple(row[amt_columns])  # Kombination der Werte in den Spalten 0-4
    values = row[amt_values_columns].tolist()  # Die Werte in den Spalten 5-9
    amt_dict[key] = values

# Debug: Prüfen, ob das amt_dict korrekt erstellt wurde
print("amt_dict erstellt mit", len(amt_dict), "Einträgen.")
print("Beispiel-Eintrag:", list(amt_dict.items())[:1])  # Ersten Eintrag anzeigen

# Definieren der neuen Spaltennamen, die am Ende der Tabelle hinzugefügt werden
new_columns = ['neuer_wert_1', 'neuer_wert_2', 'neuer_wert_3', 'neuer_wert_4', 'neuer_wert_5']

# Sicherstellen, dass die neuen Spalten existieren, und mit NaN initialisieren
for col in new_columns:
    mast_df[col] = pd.NA

# Iterieren durch die Zeilen in mast_einheitlich.csv und die Werte am Ende der Tabelle einfügen
for index, row in mast_df.iterrows():
    mast_key = tuple(row[mast_columns])  # Kombination der Werte in den Spalten 27, 29, 31, 33, 35
    
    # Debug: Anzeige des aktuellen Schlüssels und Abgleich mit amt_dict
    print(f"Zeile {index}: mast_key = {mast_key}")
    
    if mast_key in amt_dict:
        print(f"Match gefunden für mast_key: {mast_key}")
        
        # Die passenden Werte aus amt_einheitlich.csv in die neuen Spalten am Ende der Tabelle einfügen
        for i, col in enumerate(new_columns):
            mast_df.at[index, col] = amt_dict[mast_key][i]
            print(f"Setze Wert {amt_dict[mast_key][i]} in Spalte {col}")
    else:
        print(f"Kein Match für mast_key: {mast_key}")

# Neue Spalte hinzufügen für den letzten gefüllten Wert in den neuen Spalten
mast_df['letzter_gefuellter_wert'] = mast_df[new_columns].apply(
    lambda row: next((val for val in reversed(row) if pd.notna(val)), None), axis=1
)

# Speichern der aktualisierten Datei
mast_df.to_csv(output_path, sep=',', index=False)
print(f"Ergebnisse wurden in {output_path} gespeichert.")



