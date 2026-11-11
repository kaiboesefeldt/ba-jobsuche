---
name: ba-jobsuche
description: Recherchiert Stellenangebote über die inoffizielle Jobsuche-Schnittstelle der Bundesagentur für Arbeit.
---

# Stellen recherchieren

Ermittle Suchbegriffe und gegebenenfalls Orte aus dem Auftrag. Setze keine weiteren Filter als angenommene Präferenzen. Sende keine persönlichen Daten oder Bewerbungsunterlagen an die API. Führe keine Bewerbung oder Kontaktaufnahme aus.

Ermittle den absoluten Pfad zum Verzeichnis dieser SKILL.md als `SKILL_DIR`. Rufe `python3 "$SKILL_DIR/scripts/jobsuche.py" search --was 'Suchbegriff' --wo 'Ort'` auf. Für Details nutze `python3 "$SKILL_DIR/scripts/jobsuche.py" detail 'Referenznummer'`. Python 3.10 oder neuer und die Standardbibliothek genügen; das aktuelle Arbeitsverzeichnis ist unerheblich. Wiederhole die Suche gegebenenfalls mit unterschiedlichen Begriffen und führe die Ergebnisse anhand der Referenznummer zusammen. Für Heim- oder Telearbeit nutze auf ausdrücklichen Wunsch `--homeoffice`; der Filter kann sowohl hybride als auch vollständig ortsunabhängige Stellen erfassen. Prüfe in der Stellenbeschreibung den tatsächlichen Remote-Anteil und kennzeichne ihn als unklar, falls er nicht angegeben ist. Untersuche passende Details, bevor du sie bewertest.

Berichte Suchbegriffe, Quelle, Abrufzeit, Seiten und erkennbare Grenzen. Unterscheide Stelleninformationen von deiner Einschätzung und nenne Unsicherheiten. Eine erreichte Seitengrenze, Fehler oder widersprüchliche Daten bedeuten, dass Ergebnisse fehlen können. Auch sonst ist keine vollständige Momentaufnahme garantiert.
