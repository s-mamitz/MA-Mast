# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Namen von "Schöffer" zu "Schöffe" korrigieren

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:18:34 2024

@author: marcericmitzscherling
"""

import pandas as pd

# Definiere die Pfade zu den CSV-Dateien
file_paths = [
    're_1768.csv',
    're_1769.csv',
    're_1770.csv',
    're_1771.csv',
    're_1772.csv',
    're_1773.csv',
    're_1774.csv',
    're_1775.csv',
    're_1776.csv',
    're_1777.csv',
    're_1778.csv',
    're_1779.csv'
]
file_list = file_paths  # Konvertiere den String in eine Liste

# Definiere den neuen Wert für die andere Spalte
new_value = "Schöffe"  # Ersetze dies durch den gewünschten Wert

# Iteriere über die Dateipfade
for file_path in file_list:
    # Lese die CSV-Datei ein, wobei das Trennzeichen auf Semikolon gesetzt wird
    df = pd.read_csv(file_path, sep=';')

    # Suche nach "Ernst August Arnold Schöffer" in Spalte 9 (Index 8)
    mask = df.iloc[:, 9] == "Ernst August Arnold Schöffer"
    
    # Überprüfe, ob Änderungen vorgenommen werden müssen
    if mask.any():
        # Ändere den Wert in Spalte 9 (Index 8) auf "Ernst August Arnold"
        df.loc[mask, df.columns[9]] = "Ernst August Arnold"
        
        # Setze den neuen Wert in Spalte 10 (Index 9) in den gefundenen Zeilen
        df.loc[mask, df.columns[30]] = new_value  # Ersetze dies durch den gewünschten Wert

        # Ausgabe, in welcher Tabelle und in welcher Spalte eine Änderung vorgenommen wurde
        for index in df[mask].index:
            print(f"In Datei '{file_path}' wurde in Zeile {index + 1} der Wert in Spalte '{df.columns[8]}' geändert zu 'Ernst August Arnold' und in Spalte '{df.columns[9]}' geändert zu '{new_value}'.")

    # Schreibe die CSV-Datei zurück, wieder mit Semikolon als Trennzeichen
    df.to_csv(file_path, sep=';', index=False)

print("Die CSV-Dateien wurden erfolgreich aktualisiert.")


