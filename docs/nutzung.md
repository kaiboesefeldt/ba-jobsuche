# Nutzung und Schnittstelle

Python 3.10 oder neuer; zur Laufzeit ist nur die Standardbibliothek erforderlich. Vom Projektverzeichnis aus (bei einer separat bereitgestellten Skill den absoluten Pfad zu `scripts/jobsuche.py` verwenden):

```sh
python3 skills/ba-jobsuche/scripts/jobsuche.py search --was 'Softwareentwickler' --wo 'Rostock:50'
python3 skills/ba-jobsuche/scripts/jobsuche.py search --was 'Python' --size 50 --max-pages 20
python3 skills/ba-jobsuche/scripts/jobsuche.py search --was 'Python' --homeoffice 50%
python3 skills/ba-jobsuche/scripts/jobsuche.py detail 'REFERENZNUMMER'
```

`--wo 'Rostock:50'` übergibt `wo=Rostock` und `umkreis=50` (Kilometer); `query` enthält beide Parameter. Akzeptiert werden ein nicht leerer Ort und eine ganze Zahl aus ASCII-Ziffern von 0 bis 200, ohne Leerzeichen um die Zahl. Ungültige Angaben erzeugen einen Eingabefehler ohne Anfrage. Ohne Doppelpunkt wird der Ort unverändert übergeben; ohne `--wo` wird kein Ort vorgegeben. Die [Community-API-Dokumentation](https://github.com/bundesAPI/jobsuche-api) beschreibt `umkreis` in Kilometern um `wo`; die [BA-Hilfe zur Stellensuche](https://jobboerse.arbeitsagentur.de/vamJB/hilfe/de/AS/betreut/1080.html) nennt für ihre Oberfläche bis zu 200 km. Die Clientgrenze ist vorsichtig gewählt und keine Zusage für die inoffiziell dokumentierte API.

Der optionale Schalter `--homeoffice` akzeptiert `0%`, `25%`, `50%` oder `100%`; ohne Wert gilt `100%`. Andere Werte sind ein Eingabefehler. Die Werte werden auf `homeoffice=prozentual_0`, `prozentual_25`, `prozentual_50` beziehungsweise `prozentual_100` abgebildet. Ohne Schalter wird kein Homeoffice-Filter gesetzt; ohne `--wo` wird kein Ort vorgegeben. Live-Vergleiche sprechen für einen Mindestanteil, die genaue Semantik und Vollständigkeit sind jedoch nicht verbindlich dokumentiert. Angaben und Bedingungen in den Stellendetails prüfen; fehlende Angaben bleiben unklar.

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
.venv/bin/ruff check skills/ba-jobsuche/scripts scripts tests integration_tests
.venv/bin/ruff format --check skills/ba-jobsuche/scripts scripts tests integration_tests
```

Das [JSON-Schema der Ausgabe](../skills/ba-jobsuche/references/output.schema.json) beschreibt die stabile Ausgabehülle; bei Änderungen an der CLI-Ausgabe Schema, Beispiele und Schema-Tests gemeinsam aktualisieren. Die Schema-Tests validieren tatsächliche CLI-Ausgaben und ungültige Varianten mit der Entwicklungsabhängigkeit `jsonschema`; zur Laufzeit ist sie nicht erforderlich.

Die regulären Tests benötigen kein Netzwerk. Die separat auszuführenden Integrationstests greifen auf den BA-Dienst zu:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s integration_tests -v
```

Die zwei Tests senden zusammen höchstens sechs Anfragen: je eine Suche, einen allgemeinen Detailabruf und höchstens drei Detailabrufe für Homeoffice-Treffer. Sie prüfen aktuelle strukturierte Detailangaben, nicht die vertraglichen Bedingungen; fehlende oder widersprüchliche Angaben führen zum Fehlschlag. Leere Ergebnisse, Änderungen der externen Daten oder Dienstausfälle können den Test ebenfalls fehlschlagen lassen und sind gesondert zu untersuchen. Die Nutzungsbedingungen sind zu beachten.
