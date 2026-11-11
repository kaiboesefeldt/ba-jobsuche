# Implementierungsplan: Homeoffice-Filter

> Ausführung anhand des freigegebenen Entwurfs; Änderungen schrittweise mit Tests prüfen.

**Ziel:** Den Homeoffice-Filter auf die vereinbarten API-Werte umstellen und gesonderte Live-Integrationstests ergänzen.

**Architektur:** Die CLI validiert einen optionalen Prozentwert und übergibt den entsprechenden externen API-Parameter an die bestehende Suchfunktion. Die Live-Tests prüfen die CLI-Ausgabe und rufen für Suchtreffer Stellendetails ab.

**Technik:** Python 3.10+, Standardbibliothek zur Laufzeit, unittest, Coverage.py und Ruff.

**Entwurf:** `docs/superpowers/specs/2026-11-11-homeoffice-filter-design.md`

## Übergreifende Vorgaben

- Code und Tests auf Englisch; Dokumentation auf Deutsch.
- Reguläre Tests ohne Netzwerk; Live-Tests ausdrücklich separat ausführen und Anfragen begrenzen.
- Ausgabehülle und bestehendes Verhalten ohne Filter erhalten; keine unbelegte API-Garantie behaupten.
- 100 % kombinierte Anweisungs- und Zweigüberdeckung sowie Ruff-Prüfungen einhalten.

## Prüfschwerpunkte

- Fehlender Filter darf keinen Homeoffice-Parameter senden.
- Fehlender Wert nach dem Filter muss 100 % bedeuten, auch wenn weitere Optionen folgen.
- Alle vier erlaubten Angaben müssen auf die richtigen API-Werte abgebildet werden.
- Andere Werte müssen vor der Netzwerkabfrage als JSON-Eingabefehler zurückgewiesen werden.
- Leere, widersprüchliche oder geänderte Live-Antworten dürfen nicht als erfolgreicher Test gelten.

## Aufgabe 1: CLI-Filter

**Dateien:** `tests/test_cli_search.py`, `skills/ba-jobsuche/scripts/ba_jobsuche/cli.py`.

- [ ] Netzwerktests durch Mocking vermeiden; Tests für fehlendes Flag, Standardwert, `0%`, `25%`, `50%`, `100%`, nachfolgende Optionen und ungültige Eingaben schreiben. JSON-Ausgabe und Parameter des Suchaufrufs prüfen; bei Fehlern keinen Aufruf erwarten.
- [ ] Die Tests ausführen und die erwarteten Fehler der bisherigen Implementierung nachweisen.
- [ ] `--homeoffice` als optionalen Wert mit den vier zulässigen Angaben und Standard `100%` beim gesetzten Flag implementieren. In `search_command` auf `homeoffice=prozentual_<Zahl>` abbilden; ohne Flag keinen Filter setzen. Hilfetext aktualisieren.
- [ ] CLI-Tests und die reguläre Suite ausführen und Bestehen prüfen.

## Aufgabe 2: Live-Integrationstests und Dokumentation

**Dateien:** neuer separater Test unter `integration_tests/`, `docs/nutzung.md`, `skills/ba-jobsuche/SKILL.md`.

- [ ] Separate Tests schreiben, die das reale CLI-Einstiegsskript aufrufen: eine ungefilterte Suche mit maximal einer Seite und ein anschließender Detailabruf; eine Homeoffice-Suche mit maximal einer Seite und bis zu drei Detailabrufen. Ergebnisse und Referenzen prüfen; bei der Homeoffice-Stichprobe `homeofficemoeglich` und bei vorhandenem Prozentwert die Konsistenz mit dem angefragten Wert prüfen. Leere Ergebnisse und fehlende oder widersprüchliche Angaben ergeben verständliche Fehler.
- [ ] Live-Tests ausdrücklich ausführen und Ergebnisse prüfen. Netzwerkfehler und wechselnde Daten nicht als erfolgreiche Prüfung ausgeben.
- [ ] Nutzungs- und Skill-Dokumentation zu gültigen Werten, Standard, API-Abbildung, Unsicherheit und Live-Test-Aufruf aktualisieren.
- [ ] Reguläre Tests mit Coverage und Ruff-Lint/Format ausführen; den vollständigen Diff und den Branch prüfen. Einen kohärenten Commit mit Codex-Trailer erstellen, Branch über die GitHub-App pushen und einen PR zur Prüfung eröffnen; Issue #12 nennen, aber nicht automatisch schließen.
