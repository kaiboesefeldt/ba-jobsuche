# Nutzung und Schnittstelle

Python 3.10 oder neuer; zur Laufzeit ist nur die Standardbibliothek erforderlich. Vom Projektverzeichnis aus (bei einer separat bereitgestellten Skill den absoluten Pfad zu `scripts/jobsuche.py` verwenden):

```sh
python3 skills/ba-jobsuche/scripts/jobsuche.py search --was 'Softwareentwickler' --wo 'Berlin'
python3 skills/ba-jobsuche/scripts/jobsuche.py search --was 'Python' --size 50 --max-pages 20
python3 skills/ba-jobsuche/scripts/jobsuche.py search --was 'Python' --homeoffice
python3 skills/ba-jobsuche/scripts/jobsuche.py detail 'REFERENZNUMMER'
```

Der frühere Aufruf `python3 -m ba_jobsuche` aus dem Projektverzeichnis entfällt; verwende den oben angegebenen Skriptpfad.

Der optionale Schalter `--homeoffice` setzt den in der Community-Dokumentation beschriebenen API-Parameter `arbeitszeit=ho` für Heim- oder Telearbeit; ohne Schalter wird dieser Filter nicht gesetzt. Der Filter belegt keinen bestimmten Remote-Anteil: Die Stellenbeschreibung darauf prüfen und fehlende Angaben als unklar kennzeichnen. Ohne `--wo` wird kein Ort vorgegeben.

Die Suche ruft automatisch Seiten ab. Standard sind 100 Treffer pro Seite und höchstens 10 Seiten; `--size` und `--max-pages` akzeptieren Werte von 1 bis 100. Das sind Clientgrenzen, keine behaupteten Vorgaben der BA. Bei Erreichen der Seitengrenze ist `complete` falsch. `unexpected_empty_page` kennzeichnet eine vorzeitig leere Seite. `exhausted` bedeutet, dass anhand der API-Antwort keine weitere Seite erkannt wurde, nicht dass die Recherche vollständig oder eine atomare Momentaufnahme ist. `reported_totals` zeigt die pro Seite gemeldeten Trefferzahlen; sie können sich ändern. Duplikate werden anhand von `referenznummer` entfernt. Bei einem Fehler wird kein Teilergebnis als Erfolg ausgegeben.

Die JSON-Ausgabe auf stdout trägt `schema_version: 1` und `ok`. Erfolg enthält `source`, `retrieved_at` (UTC), bei Suche `query`, `results`, `pages_fetched`, `reported_totals`, `stop_reason`, `complete`, bei Details `reference` und `result`. Die Inhalte in `results` und `result` sind unveränderte externe API-Felder und können sich ändern; stabil ist die äußere Hülle. Fehler enthalten `error.code` und eine englische `error.message`; der Exit-Code ist ungleich null. Hilfetexte sind eine Ausnahme zur JSON-Ausgabe. Es werden keine Bewertungen ausgegeben.

Die [Community-Dokumentation](https://github.com/bundesAPI/jobsuche-api) beschreibt den Suchendpunkt `/pc/v6/jobs`, `was`, `wo`, `page`, `size`, `maxErgebnisse`, `ergebnisliste`, `referenznummer` und den Detailendpunkt mit Base64-kodierter Referenznummer. `page` beginnt bei 1. Ein fehlendes `ergebnisliste` wird nur bei `maxErgebnisse` 0 als leer behandelt. Diese Annahmen sind keine Stabilitätszusage und müssen bei Änderungen überprüft werden. Der automatisch gesendete öffentliche Kennwert `jobboerse-jobsuche` ist keine persönliche Anmeldung; `JOBSUCHE_API_KEY` kann ihn bei Änderungen ersetzen.

Quelle ist die Jobsuche der Bundesagentur für Arbeit; Daten und Verfügbarkeit können sich jederzeit ändern. Für den jeweiligen Einsatz sind die [BA-Nutzungsbedingungen](https://www.arbeitsagentur.de/nutzungsbedingungen) und Rechte an Inhalten zu beachten. Eine ausdrückliche Autorisierung für die automatisierte Nutzung dieser inoffiziell dokumentierten Schnittstelle ist durch die Community-Dokumentation nicht belegt. Nutzende prüfen die Bedingungen ihrer konkreten Nutzung. Persönliche Daten und Bewerbungsunterlagen nicht in Suchparametern übermitteln.

## Entwicklung

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/coverage run -m unittest discover -s tests -v
.venv/bin/coverage report
.venv/bin/ruff check skills/ba-jobsuche/scripts scripts tests
.venv/bin/ruff format --check skills/ba-jobsuche/scripts scripts tests
```

Die Tests benötigen kein Netzwerk. Ein optionaler manueller Live-Test ist ein einzelner obiger Suchaufruf mit `--max-pages 1`; er greift auf den BA-Dienst zu und setzt die Beachtung der Nutzungsbedingungen voraus.
