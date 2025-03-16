# Hinweis: Dieses Skript wurde unter Zuhilfenahme von Large Language Models (LLMs) generiert.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:54:02 2024

@author: marcericmitzscherling
"""

import os
import subprocess

# Funktionsdefinition
def run_python_scripts(script_paths):
    # Jedes Skript nacheinander ausführen
    for script_path in script_paths:
        if not os.path.exists(script_path):
            print(f"Skript {script_path} existiert nicht. Überspringe...")
            continue
        
        print(f"Starte {script_path}...")
        
        # Skript ausführen
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        
        # Ausgabe des Skripts anzeigen
        print(f"Ausgabe von {script_path}:")
        print(result.stdout)
        print(f"Fehler von {script_path}:")
        print(result.stderr)
        
        # Wenn das Skript mit einem Fehler beendet wird, abbrechen
        if result.returncode != 0:
            print(f"{script_path} wurde mit Fehlern beendet. Abbruch.")
            break
        else:
            print(f"{script_path} erfolgreich abgeschlossen.\n")

# Haupteinstiegspunkt
if __name__ == "__main__":
    # Liste der Pfade zu den Python-Skripten, die ausgeführt werden sollen
    script_paths = [
        "1 reorganize.py",
        "2 addIdSaveMaster.py",
        "3 sortTitles.py",
        #"4 titleFacet1.py",
        "4 titleFacet2.py",
        "5 splitNames.py",
        "6 cleanUpQuali.py",
        "7 extractSpezification.py",
        "8 facetQuali.py",
        "9 createMaster.py"
    ]
    
    run_python_scripts(script_paths)
