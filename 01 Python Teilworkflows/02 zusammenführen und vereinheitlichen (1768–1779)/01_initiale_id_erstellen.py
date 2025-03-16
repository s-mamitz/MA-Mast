# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Initiale ID-Spalte erzeugen

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 12:39:14 2024

@author: marcericmitzscherling
"""

import pandas as pd
import os

# Definiere die Liste der Dateipfade
# file_paths = [
#     '1768.csv',
#     '1769.csv',
#     '1770.csv',
#     '1771.csv',
#     '1772.csv',
#     '1773.csv',
#     '1774.csv',
#     '1775.csv',
#     '1776.csv',
#     '1777.csv',
#     '1778.csv',
#     '1779.csv'
# ]

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

for file_path in file_paths:
    # Lese die CSV-Datei ein
    df = pd.read_csv(file_path, sep=';', header=0)  # Kopfzeile bleibt erhalten
    
    # Lösche die gesamte erste Spalte (einschließlich der Kopfzeile)
    df.columns.values[0] = ''  # Leere den Header der ersten Spalte
    df.iloc[:, 0] = ''         # Leere die restlichen Werte in der ersten Spalte
    
    # Setze in die Kopfzeile der ersten Spalte "ID"
    df.columns.values[0] = 'ID'  # Setze die Kopfzeile der ersten Spalte auf "ID"

    # Hole den Dateinamen ohne Erweiterung
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Entferne das Präfix 're_' (falls vorhanden)
    if file_name.startswith('re_'):
        file_name = file_name[3:]  # Entferne die ersten 3 Zeichen
    
    # Fülle die erste Spalte ab der ersten Zeile mit dem Zähler im gewünschten Format
    for i in range(len(df) - 1):  # Gehe durch alle Zeilen bis zur vorletzten
        value = f"{file_name}-{i + 1:04d}"  # Beginne bei 1
        df.iloc[i, 0] = value  # Setze den Wert in der Zeile

    # Speichere die bearbeitete CSV-Datei
    df.to_csv(file_path, sep=';', index=False)





