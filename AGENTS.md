# Hinweise für die Arbeit in diesem Repository

## Ziel und Stand

Hier entsteht eine allgemein nutzbare Agent-Skill zur Recherche von Stellen über die Jobsuche der Bundesagentur für Arbeit. Änderungen sollen fachlich nachvollziehbar, verständlich und überprüfbar sein. Das Projekt befindet sich in der Konzeptionsphase.

## Zusammenarbeit

- Vor Änderungen vorhandene Dateien und den Git-Status prüfen; fremde und bereits vorhandene Änderungen erhalten.
- Anforderungen und technische Entscheidungen von Annahmen unterscheiden. Größere Änderungen vor der Umsetzung mit einem nachvollziehbaren Entwurf vorbereiten.
- Skill-Texte sowie Architektur- und Designdokumentation auf Deutsch verfassen. Code einschließlich Bezeichnern, Kommentaren, Docstrings und Fehlermeldungen auf Englisch schreiben; vorgegebene externe API-Feldnamen und Parameter unverändert übernehmen.
- Auf eigenen Arbeitsbranches nach eigenem Ermessen committen und pushen.

## Branches und Pull Requests

- Änderungen auf einem eigenen Branch vorbereiten; nicht direkt auf `main` arbeiten oder dorthin pushen.
- Änderungen über einen Pull Request zur Prüfung vorlegen. Der Nutzer entscheidet über Freigabe und Merge; Review-Rückmeldungen auf dem PR-Branch bearbeiten. Nicht eigenständig mergen.
- KI-Unterstützung bei von Codex erstellten Commits durch den Trailer `Assisted-by: OpenAI Codex` kenntlich machen. Im Pull Request kurz darstellen, welche Umsetzung von Codex stammt und welche wesentlichen Vorgaben oder Entscheidungen vom Nutzer kommen.
- Für GitHub-Aktionen die vorgesehene GitHub-App-Identität verwenden.

## Entwicklung

- Für Laufzeitcode möglichst ausschließlich die Python-Standardbibliothek verwenden; zusätzliche Laufzeitabhängigkeiten besonders streng begründen. Die unterstützte Python-Version ist noch festzulegen.
- Ruff als Entwicklungsabhängigkeit für Linting und Formatierung einsetzen; Konfiguration und Ausführung bei der Implementierung dokumentieren.
- Projektbeiträge stehen unter Apache License 2.0; Rechte und Bedingungen für eingebundene Materialien und externe Daten gesondert beachten.
- API-Zugriff, Suchlogik und CLI trennen; ein eigenes stabiles CLI-Ausgabeformat definieren. Schnittstellen und Fehlerfälle ausdrücklich behandeln und unnötige Komplexität vermeiden.
- Änderungen mit geeigneten, aussagekräftigen Tests überprüfen. Tests sollen grundsätzlich ohne Netzwerk ausführbar sein; optionale Live-Prüfungen gesondert kennzeichnen und begrenzen.
- Die Community-Dokumentation der API ist keine Stabilitätszusage. Annahmen über Parameter, Antwortformate und Seitennavigation dokumentieren und bei Änderungen prüfen.
- Suchergebnisse und Bewertungen trennen; Quellen, Aktualität und erkennbare Grenzen einer Recherche nennen. Suchfilter nicht ohne Grundlage als Nutzerpräferenz setzen.
- Personenbezogene Daten und Bewerbungsunterlagen nicht an die Jobsuche-API senden oder als Testdaten einchecken. Die Skill führt keine Bewerbung oder Kontaktaufnahme eigenständig aus.
- README kurz halten und bei belegbaren Änderungen aktualisieren; ausführliche Dokumentation strukturiert unter `docs/` ablegen.
