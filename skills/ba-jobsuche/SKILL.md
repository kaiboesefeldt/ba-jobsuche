---
name: ba-jobsuche
description: Verwende diese Skill für die Suche nach Jobs und Stellenangeboten beim Suchservice der Bundesagentur für Arbeit.
---

# Stellen recherchieren

Die Skill benötigt Python 3.10 oder neuer und Netzwerkzugriff auf die Jobsuche der Bundesagentur für Arbeit; zusätzliche Python-Pakete sind nicht erforderlich.

## Aufruf

Suche Stellen und rufe Details mit `scripts/jobsuche.py` ab:

```sh
python3 scripts/jobsuche.py search --was 'Suchbegriff' --wo 'Rostock:50' --homeoffice 25%
python3 scripts/jobsuche.py detail 'Referenznummer'
```

`--wo` akzeptiert einen Ort oder `Ort:Kilometer` mit ganzzahligem Umkreis von 0 bis 200 km; ohne `--wo` wird kein Ort vorgegeben. Ungültige Angaben führen zu einem Eingabefehler. Die API-Grenzen sind nicht verbindlich dokumentiert.

`--homeoffice` akzeptiert optional `0%`, `25%`, `50%` oder `100%`; ohne Wert gilt `100%`.

Weitere Parameter beschreibt `--help` beim jeweiligen Unterbefehl.

```sh
python3 scripts/jobsuche.py search --help
python3 scripts/jobsuche.py detail --help
```

## Ausgabeformat

Das Skript gibt JSON auf der Standardausgabe aus. Wird die Option `--help` übergeben, ist die Ausgabe ein Hilfetext.

Es folgen Beispiele für Ausgaben der Kommandos `search` und `detail`. Sie enthalten fiktive Daten. Die Felder innerhalb von `results` und `result` können variieren.

### Beispiel für `search`

```json
{
  "schema_version": 1,
  "ok": true,
  "source": "https://www.arbeitsagentur.de/jobsuche/",
  "retrieved_at": "2026-01-01T12:00:00+00:00",
  "query": {"was": "Softwareentwicklung", "wo": "Berlin", "homeoffice": "25%"},
  "results": [{"referenznummer": "BEISPIEL-123", "titel": "Softwareentwickler"}],
  "pages_fetched": 1,
  "reported_totals": [1],
  "stop_reason": "exhausted",
  "complete": true
}
```

### Beispiel für `detail`

```json
{
  "schema_version": 1,
  "ok": true,
  "source": "https://www.arbeitsagentur.de/jobsuche/",
  "retrieved_at": "2026-01-01T12:00:00+00:00",
  "reference": "BEISPIEL-123",
  "result": {"titel": "Softwareentwickler", "stellenbeschreibung": "Fiktive Stellenbeschreibung"}
}
```

### JSON-Schema der Ausgabe

Das [JSON-Schema](references/output.schema.json) beschreibt die stabile Ausgabehülle für Suche, Detailabfrage und Fehler. Die Felder der Schnittstelle können variieren.

## Fehlerbehandlung

Bei Fehlern hat `ok` den Wert `false` und der Exit-Code ungleich null; es wird kein Teilergebnis ausgegeben.

Eine erreichte Seitengrenze, Fehler oder widersprüchliche Daten bedeuten, dass Ergebnisse fehlen können. Auch sonst ist keine vollständige Momentaufnahme garantiert.

# Hinweis

Sende keine persönlichen Daten oder Bewerbungsunterlagen an die Schnittstelle.
