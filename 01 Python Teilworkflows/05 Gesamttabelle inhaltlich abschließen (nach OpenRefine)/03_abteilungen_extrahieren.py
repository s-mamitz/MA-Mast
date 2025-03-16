# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Extrahiert und speichert Abteilungsinformationen einheitlich.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 14:33:06 2024

@author: marcericmitzscherling
"""

import pandas as pd

# CSV-Datei einlesen
file_path = 'amt_namen_ma-mast_aktualisiert_einheitlich.csv'
df = pd.read_csv(file_path, sep=',')  # Komma als Separator

# Die interessierenden Spalten
columns_to_consider = [63, 64, 65, 66, 67]

# DataFrame für die Kombinationen erstellen
# Wir kombinieren die Werte der genannten Spalten zu einem einzigen DataFrame
combinations = df.iloc[:, columns_to_consider].drop_duplicates()

# Eine neue Tabelle erstellen, die die einzigartigen Kombinationen enthält
unique_combinations = combinations.drop_duplicates()

# Speichern der einzigartigen Kombinationen in eine neue CSV-Datei
output_file_path = 'import_abteilungskombinationen_einheitlich.csv'
unique_combinations.to_csv(output_file_path, index=False, sep=',')

