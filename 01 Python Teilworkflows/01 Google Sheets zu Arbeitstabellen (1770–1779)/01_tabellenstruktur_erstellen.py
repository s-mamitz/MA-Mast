# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:06:43 2024

@author: marcericmitzscherling
"""

import pandas as pd
import os

# Liste der CSV-Dateien, die verarbeitet werden sollen
csv_files = ['1771.csv','1772.csv','1773.csv','1774.csv','1775.csv','1776.csv','1777.csv','1778.csv','1779.csv']  # Hier deine CSV-Dateien einfügen

# Funktion zur Bearbeitung einer einzelnen Datei
# Funktionsdefinition
def process_csv(file_path):
    # CSV-Datei laden
    df = pd.read_csv(file_path, delimiter=';')

    # Zeilen löschen, bei denen Spalte 8 keinen Wert hat oder 'weg' steht
    df = df.dropna(subset=[df.columns[7]])  # Spalte 8 (index 7)
    df = df[df[df.columns[7]] != 'weg']
    
    # Prüfen, wie viele Spalten die Input-Tabelle hat
    num_columns = len(df.columns)

    if num_columns <= 22:

        # Neue DataFrame mit den gewünschten 22 Spalten anlegen
        output_columns = ['ID', 'ID alt', 'Anrede', 'Anredetitel', 'Akademischer Grad', 
                          'Militärischer (Dienst-)Grad', 'Adelstitel', 'N1', 'N2', 'Name', 
                          'Veränderung', 'V1', 'V2', 'V3', 'V4', 'V5', 'N', 
                          'genannt', 'unmittelbare Anstellung', 'Q (unmittelbare Anstellung)', 
                          'Q1', 'Q1 Spez', 'Q2', 'Q2 Spez', 'Q3', 'Q3 Spez', 
                          'Q4', 'Q4 Spez', 'Q5', 'Q5 Spez']
    
        output_df = pd.DataFrame(columns=output_columns)
    
        # Werte aus der Input-Tabelle in die Output-Tabelle übertragen
        output_df['ID'] = ''  # Spalte 1 neu anlegen
        output_df['ID alt'] = df[df.columns[0]]  # Spalte 2 aus Spalte 1 der Input-Tabelle
        output_df['Anrede'] = ''  # Spalte 3 neu anlegen
        output_df['Anredetitel'] = ''  # Spalte 4 neu anlegen
        output_df['Akademischer Grad'] = ''  # Spalte 5 neu anlegen
        output_df['Militärischer (Dienst-)Grad'] = ''  # Spalte 6 neu anlegen
        output_df['Adelstitel'] = ''  # Spalte 7 neu anlegen
        
        # Füge Spalten 15 und 16 der Input-Tabelle in die Output-Tabelle vor der Spalte "Name" hinzu
        output_df['N1'] = df[df.columns[14]]  # Spalte 8 aus Spalte 15 der Input-Tabelle
        output_df['N2'] = df[df.columns[15]]  # Spalte 9 aus Spalte 16 der Input-Tabelle
        output_df['Name'] = df[df.columns[6]]  # Spalte 10 aus Spalte 7 der Input-Tabelle
        
        output_df['Veränderung'] = df[df.columns[7]]  # Spalte 11 aus Spalte 8 der Input-Tabelle
        output_df['V1'] = df[df.columns[16]]  # Spalte 12 aus Spalte 17 der Input-Tabelle
        output_df['V2'] = df[df.columns[17]]  # Spalte 13 aus Spalte 18 der Input-Tabelle
        output_df['V3'] = df[df.columns[18]]  # Spalte 14 aus Spalte 19 der Input-Tabelle
        output_df['V4'] = df[df.columns[19]]  # Spalte 15 aus Spalte 20 der Input-Tabelle
        output_df['V5'] = df[df.columns[20]]  # Spalte 16 aus Spalte 21 der Input-Tabelle
        output_df['N'] = df[df.columns[21]]  # Spalte 16 aus Spalte 21 der Input-Tabelle
        output_df['genannt'] = ''  # Spalte 17 neu anlegen
        output_df['unmittelbare Anstellung'] = df[df.columns[1]]  # Spalte 18 aus Spalte 2 der Input-Tabelle
        output_df['Q (unmittelbare Anstellung)'] = df[df.columns[2]]  # Spalte 19 aus Spalte 3 der Input-Tabelle
    
        # Q1 bis Q5 und deren Spez-Spalten
        for i in range(8, 13):  # Spalten 9-13 (0-indexiert) entsprechen Q1-Q5
            output_df[f'Q{i-7}'] = df[df.columns[i]]
            output_df[f'Q{i-7} Spez'] = ''
            
    else:
        # Falls die Tabelle mehr als 22 Spalten hat
        output_columns = ['ID', 'ID alt', 'Anrede', 'Anredetitel', 'Akademischer Grad', 
                          'Militärischer (Dienst-)Grad', 'Adelstitel', 'N1', 'N2', 'Name', 
                          'Veränderung', 'V1', 'V2', 'V3', 'V4', 'V5', 
                          'N', 'genannt', 'unmittelbare Anstellung', 'Q (unmittelbare Anstellung)', 
                          'Q1', 'Q1 Spez', 'Q2', 'Q2 Spez', 'Q3', 'Q3 Spez', 
                          'Q4', 'Q4 Spez', 'Q5', 'Q5 Spez', 'Q6', 'Q6 Spez']

        output_df = pd.DataFrame(columns=output_columns)

        output_df['ID'] = ''  # Spalte 1 neu anlegen
        output_df['ID alt'] = df[df.columns[0]]  # Spalte 2 aus Spalte 1 der Input-Tabelle
        output_df['Anrede'] = ''  # Spalte 3 neu anlegen
        output_df['Anredetitel'] = ''  # Spalte 4 neu anlegen
        output_df['Akademischer Grad'] = ''  # Spalte 5 neu anlegen
        output_df['Militärischer (Dienst-)Grad'] = ''  # Spalte 6 neu anlegen
        output_df['Adelstitel'] = ''  # Spalte 7 neu anlegen

        output_df['N1'] = df[df.columns[17]]  # Spalte 8 aus Spalte 18 der Input-Tabelle
        output_df['N2'] = df[df.columns[18]]  # Spalte 9 aus Spalte 19 der Input-Tabelle
        output_df['Name'] = df[df.columns[6]]  # Spalte 10 aus Spalte 7 der Input-Tabelle
        output_df['Veränderung'] = df[df.columns[7]]  # Spalte 11 aus Spalte 8 der Input-Tabelle
        output_df['V1'] = df[df.columns[19]]  # Spalte 12 aus Spalte 20 der Input-Tabelle
        output_df['V2'] = df[df.columns[20]]  # Spalte 13 aus Spalte 21 der Input-Tabelle
        output_df['V3'] = df[df.columns[21]]  # Spalte 14 aus Spalte 22 der Input-Tabelle
        output_df['V4'] = df[df.columns[22]]  # Spalte 15 aus Spalte 23 der Input-Tabelle
        output_df['V5'] = df[df.columns[23]]  # Spalte 16 aus Spalte 24 der Input-Tabelle
        output_df['N'] = df[df.columns[24]]  # Spalte 17 aus Spalte 25 der Input-Tabelle
        output_df['genannt'] = ''  # Spalte 18 neu anlegen
        output_df['unmittelbare Anstellung'] = df[df.columns[1]]  # Spalte 19 aus Spalte 2 der Input-Tabelle
        output_df['Q (unmittelbare Anstellung)'] = df[df.columns[2]]  # Spalte 20 aus Spalte 3 der Input-Tabelle

        # Q1 bis Q7 und deren Spez-Spalten
        for i in range(8, 15):  # Spalten 9-14 (0-indexiert) entsprechen Q1-Q7
            output_df[f'Q{i-7}'] = df[df.columns[i]]
            output_df[f'Q{i-7} Spez'] = ''

    # Die bearbeitete Datei speichern
    output_file_path = f're_{os.path.basename(file_path)}'
    output_df.to_csv(output_file_path, sep=';', index=False)
    print(f'Processed {file_path} and saved to {output_file_path}')

# Alle CSV-Dateien verarbeiten
for file in csv_files:
    process_csv(file)
