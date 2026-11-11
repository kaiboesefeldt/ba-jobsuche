---
name: ba-jobsuche
description: Verwende diese Skill für die Stellensuche und Stellenangebote der Bundesagentur für Arbeit.
---

# Stellen recherchieren

Ermittle Suchbegriffe und gegebenenfalls Orte aus dem Auftrag. Setze keine weiteren Filter als angenommene Präferenzen. Sende keine persönlichen Daten oder Bewerbungsunterlagen an die Schnittstelle. Führe keine Bewerbung oder Kontaktaufnahme aus.

Die Skill benötigt Python 3.10 oder neuer und Netzwerkzugriff auf die Jobsuche der Bundesagentur für Arbeit; zusätzliche Python-Pakete sind nicht erforderlich. Suche Stellen und rufe Details mit `scripts/jobsuche.py` ab:

```sh
python3 scripts/jobsuche.py search --was 'Suchbegriff' --wo 'Ort'
python3 scripts/jobsuche.py detail 'Referenznummer'
```

Die Ausgabe ist JSON mit `schema_version` und `ok`; bei Fehlern enthält sie `error` und der Exit-Code ist ungleich null. Wiederhole die Suche gegebenenfalls mit unterschiedlichen Begriffen und führe die Ergebnisse anhand der Referenznummer zusammen. Für Heim- oder Telearbeit nutze auf ausdrücklichen Wunsch `--homeoffice`; der Filter kann sowohl hybride als auch vollständig ortsunabhängige Stellen erfassen. Prüfe in der Stellenbeschreibung den tatsächlichen Remote-Anteil und kennzeichne ihn als unklar, falls er nicht angegeben ist. Untersuche passende Details, bevor du sie bewertest.

Berichte Suchbegriffe, Quelle, Abrufzeit, Seiten und erkennbare Grenzen. Unterscheide Stelleninformationen von deiner Einschätzung und nenne Unsicherheiten. Eine erreichte Seitengrenze, Fehler oder widersprüchliche Daten bedeuten, dass Ergebnisse fehlen können. Auch sonst ist keine vollständige Momentaufnahme garantiert.
