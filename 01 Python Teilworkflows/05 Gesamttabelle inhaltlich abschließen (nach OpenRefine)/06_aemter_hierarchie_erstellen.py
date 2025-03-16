# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
# Erstellt und speichert eine Hierarchie der Ämter.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:19:47 2024

@author: marcericmitzscherling
"""

import pandas as pd
import numpy as np  # Importiere das NumPy-Modul
import sys  # Importiere das sys-Modul

# CSV-Dateien einlesen
abteilungen_df = pd.read_csv('abteilungen_einheitlich.csv')
qid_amt_df = pd.read_csv('qid-amt_einheitlich.csv')

# Erstelle ein Dictionary für die Ersetzungen
replacement_dict = dict(zip(qid_amt_df.iloc[:, 0], qid_amt_df.iloc[:, 1]))

# Ersetze die Werte in der abteilungen_einheitlich.csv
def replace_values(df, replacement_dict):
    replaced = True
    not_found = []

    for col in df.columns:
        for index in df.index:
            original_value = df.at[index, col]
            if pd.isna(original_value):  # Ignoriere NaN-Werte
                continue
            if original_value in replacement_dict:
                df.at[index, col] = replacement_dict[original_value]
            else:
                not_found.append(original_value)
                replaced = False

    return replaced, not_found

# Werte ersetzen
replaced, not_found = replace_values(abteilungen_df, replacement_dict)

# Überprüfe, ob alle Werte ersetzt wurden
if not replaced:
    not_found_set = set(not_found) - {np.nan}  # Entferne NaN aus der Liste
    if not_found_set:
        print("Folgende Werte in abteilungen_einheitlich.csv wurden nicht gefunden:")
        print(not_found_set)
    sys.exit()  # Beende das Skript

# Überprüfe, ob alle Werte in qid-amt_einheitlich.csv verwendet wurden
unused_values = set(qid_amt_df.iloc[:, 1]) - set(replacement_dict.values())
if unused_values:
    print("Folgende Werte in qid-amt_einheitlich.csv wurden nicht verwendet:")
    print(unused_values)
    sys.exit()  # Beende das Skript

# Funktion zur Ermittlung der Hierarchieführer
def get_hierarchy(df):
    hierarchy = {}
    
    # Iteriere über jede Zeile
    for index, row in df.iterrows():
        for i in range(len(row)):
            if pd.isna(row[i]):  # Ignoriere NaN-Werte
                continue
            leader = row[i]
            if leader not in hierarchy:
                hierarchy[leader] = []
            if i + 1 < len(row) and not pd.isna(row[i + 1]):
                hierarchy[leader].append(row[i + 1])
    
    return hierarchy

# Funktion zur Erstellung der umgekehrten Hierarchietabelle
def create_reversed_hierarchy_table(hierarchy):
    reversed_rows = []
    
    for leader, subordinates in hierarchy.items():
        # Umkehren der Hierarchie
        for subordinate in subordinates:
            reversed_rows.append([subordinate, leader])  # Untergebene zuerst, dann Führer
    
    # Erstelle ein DataFrame aus den umgekehrten Zeilen
    reversed_df = pd.DataFrame(reversed_rows, columns=['Subordinate', 'Leader']).dropna()
    
    # Sortiere nach der Anzahl der Subordinate (absteigend)
    reversed_df['Count'] = reversed_df.groupby('Leader')['Subordinate'].transform('count')  # Zähle die Anzahl der Subordinate
    reversed_df = reversed_df.sort_values(by='Count', ascending=False).drop(columns='Count')  # Sortiere und entferne die Zählspalte
    
    return reversed_df

# Erhalte die Hierarchie
hierarchy = get_hierarchy(abteilungen_df)

# Erstelle die umgekehrte Hierarchietabelle
reversed_table = create_reversed_hierarchy_table(hierarchy)

# Ausgabe der umgekehrten Hierarchietabelle
print(reversed_table)

# Optional: Speichere die umgekehrte Hierarchietabelle in eine neue CSV-Datei
reversed_table.to_csv('umgekehrte_hierarchie_tabelle_einheitlich.csv', index=False, header=False)
