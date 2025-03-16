# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:30:47 2024

@author: marcericmitzscherling
"""

import pandas as pd
import re

# Pfade zu den Tabellen
table_paths = [    
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

# GREL Ersetzungswerte
replacements_stage_4 = {
    "Cammer": "Kammer",
    "ecretarius": "ekretär",
    "ecetarius": "ekretär",
    "Secretarii": "Sekretär",
    "Sekretarii": "Sekretär",
    "Secret.": "Sekretär",
    "ector": "ektor",
    "unct": "unkt",
    "othe": "ote",
    "gius": "g",
    "gus": "g",
    "car": "kar",
    "ius": "",
    "arius": "ar",
    "ath": "at",
    "cco": "kko",
    "co": "ko",
    "ca": "ka",
    "Ca": "Ka",
    "cce": "kze",
    "ce": "ze",
    "cu": "ku",
    "coll": "koll",
    "irer": "ierer",
    "irung": "ierung",
    "ceptor": "zeptor",
    "ccess": "kzess",
    "tus": "t",
    "Act": "Akt",
    "Co": "Ko",
    "robbe": "robe",
    "Oe": "Ö",
    "mus": "m",
    "nus": "n",
    "cie": "zie",
    "cäm": "käm",
    "Cäm": "Käm",
    "dant": "tant",
    "ellist": "list",
    "prae": "prä",
    "kaß": "kass",
    "ectur": "ektur",
    "oleur": "olleur",
    "miß": "miss",
    "Commiss": "Kommiss",
    "commiss": "kommiss",
    "factor": "faktor",
    "Factor": "Faktor",
    "schmiedt": "schmied",
    "actuar": "aktuar",
    "pursche": "bursche",
    "Vice": "Vize",
    "Viece": "Vize",
    "Vieze": "Vize",
    "reuter": "reiter",
    "Renth": "Rent",
    "renth": "rent",
    "Laquay": "Lakai",
    "laquay": "lakai",
    "controleur": "kontrolleur",
    "Schloß": "Schloss",
    "Stucca": "Stucka",
    "Fändrich": "Fähnrich",
    "bötger": "böttcher",
    "Zigel": "Ziegel",
    "Hautboist": "Oboist",
    "mahler": "maler",
    "ifft": "ift",
    "eometra": "eometer",
    "schwerdiger": "schwertfeger",
    "Jagt": "Jagd",
    "bedienter": "diener",
    "mädgen": "mädchen",
    "Mädgen": "Mädchen",
    "Kapitaine": "Capitaine",
    "Obrister": "Obrist",
    "tekar": "thekar",
    "afier": "affier",
    "schwerdieger": "schwertfeger",
    "voigt": "vogt",
    "Voigt": "Vogt",
    "Gallikae": "Gallicae",
    "Mäurer": "Maurer",
    "waradein": "wardein",
    "ord.": "ordentlicher",
    "ord ": "ordentlicher ",
    "Paucker": "Pauker",
    "emerit": "emeritus",
    "kommantant": "kommandant",
    "Kommantant": "Kommandant",
    "kapitain": "capitain",
    "Kapitain": "Capitain",
    "Schöffer": "Schöffe",
    "Thor": "Tor",
    "Unter ": "Unter",
    "Wagenhaler": "Wagenhalter",
    "StadtMusikus instrument": "Stadtmusikusinstrument",
    "Zucht und Armenhaus Verwalter": "Zucht- und Armenhausverwalter",
    "Kabinets": "Kabinetts",
    "Wirlich": "Wirklich",
    "Geh.": "Geheimer",
    "Legat. ": "Legations",
    "Legat.": "Legations",
    "ey": "ei"
}
replacements_stage_5 = {
    "Amt ": "Amts",
    "Amts ": "Amts",
    "Rats ": "Rats",
    "Rat ": "Rats",
    "Regiments ": "Regiments",
    "Hof ": "Hof",
    "Reise ": "Reise",
    "Archiv ": "Archiv",
    "Lehns ": "Lehns",
    "Gerichts ": "Gerichts",
    "Regierungs ": "Regierungs"
}

# Ersetzungsregeln für die benachbarten Spalten
replacements_right_columns = {
    r"^zu ": "",
    r"zur ": "",
    r"beim ": "",
    r"im ": "",
    r"bei der ": "",
    r"von der ": "",
    r"(?i)stadt\s": "",  # Das (?i) sorgt für case-insensitive matching
    r"^(auf der )(.+?)( Stube)$": r"Stube von \2",
    r"^des\s+(\w+?)(es|s)\s*": r"\1 ",
    r"^eines\s+(\w+?)(es|s)\s*": r"\1 "
}

# Hilfsfunktion zur Anwendung der GREL-Anweisungen auf die Spalten ab Spalte 21
# Funktionsdefinition
def apply_grel_transformations(value):
    # Stufe 3: Initiale Transformationen
    value = value.replace("- ", "-").replace(" -", "-").replace(" - ", "-")
    value = re.sub(r"-([A-Z])", r"\1", value)
    if " " not in value:
        value = value.title()
    
    # Stufe 4: Ersetzungen aus replacements_stage_4
    for old, new in replacements_stage_4.items():
        value = value.replace(old, new)
    
    # Stufe 5: Ersetzungen aus replacements_stage_5
    for old, new in replacements_stage_5.items():
        value = value.replace(old, new)
    
    # Stufe 6: Wenn kein Leerzeichen, Umwandlung in Titelcase
    if " " not in value:
        value = value.title()
    
    return value

# Funktion zur Anwendung der Ersetzungen auf die benachbarten Spalten
# Funktionsdefinition
def apply_grel_right_column_transformations(value):
    for pattern, replacement in replacements_right_columns.items():
        value = re.sub(pattern, replacement, value)
    return value

# Hauptskript zur Bearbeitung der Tabellen
for table_path in table_paths:
    # Tabelle einlesen
    df = pd.read_csv(table_path, sep=';')
    
    # Iteriere über die Spalten ab Spalte 21 und jede zweite danach
    for col in df.columns[21::2]:
        df[col] = df[col].apply(lambda x: apply_grel_transformations(str(x)) if pd.notnull(x) else x)

    # Bearbeite die benachbarten (rechts nebenstehenden) Spalten
    for col in df.columns[22::2]:
        df[col] = df[col].apply(lambda x: apply_grel_right_column_transformations(str(x)) if pd.notnull(x) else x)
    
    # Tabelle unter dem ursprünglichen Dateinamen speichern (überschreiben)
    df.to_csv(table_path, sep=';', index=False)