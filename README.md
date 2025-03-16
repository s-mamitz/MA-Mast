
# MA-Mast 
## Einführung
Dieses Repository bildet paradigmatisch und rein-illustriativ im Rahmen der Masterarbeit mit dem Titel **Vom _Hof= und Adreß=Calender_ zum Datensatz. Gewinnung, Modellierung und Exploration prosopographisch-organisatorischer Daten frühneuzeitlicher serieller Quellen** entstandene Python-Skripte zur Verfügung. Weitere Informationen sowie die entstandenen Datensätze finden sich auf der [FactGrid-Projektseite der Arbeit](https://database.factgrid.de/wiki/FactGrid:Amtskalender_Herzogtum_Sachsen-Gotha-Altenburg). 
> Alle im Projekt verwendeten Skripte wurden unter Zuhilfenahme von _LLMs_ wie GPT-4o oder Claude Haiku 3 erstellt

## Repository-Struktur
```
MA-Mast/
├── 01 Python Teilworkflows/
│   ├── 01 Google Sheets zu Arbeitstabellen (1770–1779)
│   │   └── (Einzelskripte)
│   ├── 02 zusammenführen und vereinheitlichen (1768–1779)
│   │   └── (Einzelskripte)
│   ├── 03 Gesamttabelle bearbeiten (neben OpenRefine)
│   │   └── (Einzelskripte)
│   ├── 04 Gesamttabelle auf Konsistenz überprüfen (neben OpenRefine)
│   │   └── (Einzelskripte)
│   ├── 05 Gesamttabelle inhaltlich abschließen (nach OpenRefine)
│   │   └── (Einzelskripte)
│   └── 06 Importtabellen erstellen (Amtsbezeichnungen, Amtsstellen)
│   │   └── (Einzelskripte)
├── 02 Deepnote/
│   ├── Deskriptive-Analyse/
│   │   └── (Notebooks und Requirements)
│   └── Explorative-Analyse/
│   │   └── (Notebooks und Requirements)
└── README.md
```
### Python-Teilworkflows
Dieses Repository enthält zum einen ausgewählte Skripte der für die Masterarbeitarbeit erstellten und verwendeten Python-Teilworkflows. Aufgabe dieser ist lediglich paradigmatisch die Bearbeitungsschritte der durch einen _Citizen Scientist_ erhobenen Amtskalenderdaten nachvollziehbar zu machen. Teilweise wurden Datensätze manuell bearbeitet, bauten auf Datenbereinigungen in OpenRefine auf oder zogen temporäre Dateien hinzu. Diese Schritte können im Repository nicht abgebildet werden, sodass die hier zur Verfügung gestellten Skripte ledigliche illustrativen, aber keinen produktiven Charakter haben. Das Dateinamenmanagement wurde maschinell angepasst, um den  Workflow übersichtlicher zusammenzuführen. So können unter umständen Interferenzen entstanden sein!
### Deepnote Visualisierungen
Zum anderen stellt dieses Repository die in Deepnote verwendeten _Data Science Notebooks_ zu Zwecken der Dokumentation, Transparenz und Adaption zur Verfügung. 
## Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen findest du in der LICENSE-Datei.
