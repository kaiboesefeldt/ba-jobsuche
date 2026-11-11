# Bündelung des Laufzeitcodes in der Skill

## Ziel und Grenzen

Die Skill ist mit Python ab 3.10 und der Standardbibliothek samt Suche und Detailabfrage separat nutzbar. Ausgabeformat, Suchverhalten und Trennung von API, Suche und CLI bleiben erhalten. Eine allgemeine Installationsanleitung gehört zu Issue #6.

## Varianten und Entscheidung

Ein gemeinsames Paket im Skill-Verzeichnis vermeidet eine zweite Kopie und lässt die bisherigen Modulgrenzen bestehen. Ein eigenständiges monolithisches Skript würde diese Grenzen auflösen; eine Kopie des Pakets im Repository und in der Skill müsste synchron gehalten werden. Daher liegt das einzige Paket unter `skills/ba-jobsuche/scripts/ba_jobsuche`; `scripts/jobsuche.py` startet dessen CLI. Der absolute Skriptpfad macht den Aufruf unabhängig vom Arbeitsverzeichnis und funktioniert auch bei Leerzeichen im Pfad.

## Prüfung

Die vorhandenen netzwerkfreien Tests prüfen Suche, Details, Fehler und Ausgabeformat. Ein zusätzlicher Prozess-Test kopiert die Skill isoliert und startet sie aus einem anderen Verzeichnis mit bereinigtem Python-Suchpfad. Die Projektanleitung dokumentiert den geänderten Aufruf; die Skill verweist nicht auf Dateien außerhalb ihres Ordners.
