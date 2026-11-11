# Implementierungsplan BA-Jobsuche

Ziel: Persönliche Recherche über die inoffizielle API mit stabiler JSON-CLI und deutschsprachiger Skill. Grundlage: `docs/superpowers/specs/2026-11-11-ba-jobsuche-design.md` und die abgestimmte automatische Seitennavigation.

1. API-Client: HTTPS, öffentlicher Kennwert, Zeitlimit, kontrollierte Fehler und Detailabruf; netzwerkfreie Tests mit simulierten Antworten.
2. Suche: Seiten nacheinander abrufen, Referenznummern deduplizieren, Grenze und Abbruchgrund ausweisen; Tests für leere, fehlerhafte, begrenzte und wechselnde Ergebnisse.
3. CLI: versionierte JSON-Erfolge und -Fehler, Eingabevalidierung, Suchparameter und Details; Aufruftests ohne Netzwerk.
4. Skill, API-Annahmen, Nutzungs- und Entwicklungsdokumentation sowie Ruff-Konfiguration ergänzen. Gesamtsuite, Ruff und Ausgabe prüfen.

Python 3.10+, Laufzeit nur Standardbibliothek; Code Englisch, Dokumentation Deutsch. Die Standardgrenze von 10 Seiten ist eine veränderbare Vorsichtsgrenze des Clients, keine BA-Vorgabe. Abrufe sind keine atomare Momentaufnahme.
