# Kombinierte Suche – Implementierungsplan

**Ziel:** Issue #10 mit unverändertem Ausgabe-Schema umsetzen.
**Architektur:** Vorvalidierte kartesische Kombinationen nutzen die bestehende Seitensuche; Ergebnisse und Metadaten werden zusammengefasst.
**Technik:** Python 3.10+, Standardbibliothek; Offline-Unittests.
**Entwurf:** `docs/superpowers/specs/2026-11-12-kombinierte-suche-design.md`

- [ ] Tests für Kombinationen, Deduplizierung, Ortlosigkeit, Seitengrenzen, Fehler und ungültige Eingaben zuerst schreiben und fehlschlagen sehen.
- [ ] CLI und Zusammenführung implementieren; Einzelaufrufe kompatibel halten.
- [ ] Nutzung, Skill und Schema-Beschreibungen aktualisieren; Schema selbst unverändert lassen.
- [ ] Tests, Zweigüberdeckung, Ruff und Diff prüfen; eigenen Branch zur Prüfung vorlegen.
