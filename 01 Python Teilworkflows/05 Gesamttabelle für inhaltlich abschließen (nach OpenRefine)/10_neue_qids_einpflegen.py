# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Pflegt neue Q-IDs systematisch in die bestehenden Datensätze ein.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:22:32 2024

@author: marcericmitzscherling
"""

import pandas as pd

# CSV-Dateien einlesen
master_df = pd.read_csv("2_1_master_einheitlich.csv", header=None)
import_df = pd.read_csv("3 import qids_einheitlich.csv", header=None)

# Über IDs aus der Import-Datei iterieren
for _, import_row in import_df.iterrows():
    import_id = import_row[1]  # ID in der Importdatei in Spalte 1
    import_value = import_row[0]  # Wert in Spalte 0 der Importdatei

    # Zeile in der Master-Tabelle finden, die die gleiche ID enthält
    matching_rows = master_df[master_df[0] == import_id]

    # Wenn eine Übereinstimmung gefunden wird, aktualisiere Spalte 3 der Master-Tabelle
    for idx in matching_rows.index:
        master_df.at[idx, 3] = import_value

# Aktualisierte Master-Tabelle speichern
master_df.to_csv("3_2_1_master_einheitlich.csv", index=False, header=False)
