# Entwurf: Homeoffice ohne Prozentangabe

Issue #26 ergänzt die Suche mit Prozentfilter um eine ausdrückliche Wahl, ob Stellen mit Homeoffice-Möglichkeit ohne strukturierte Prozentangabe einbezogen werden. Ohne neue Option bleibt das bisherige Verhalten erhalten. Ein fehlender Wert ist kein bestimmter Anteil; die Ergebnisse bleiben unveränderte API-Daten.

## Ansätze und Grundlage

Das BA-Frontend übermittelt beim Ausblenden den Wert `prozentual_100`, beim Einbeziehen `prozentual_100;nv_true` im Parameter `homeoffice`. Der vom Nutzer bereitgestellte Netzwerkvergleich zeigt für dieselbe Suche 21 beziehungsweise 522 Treffer; die zusätzlichen Treffer auf der ersten Seite tragen `homeofficetyp: NACH_VEREINBARUNG` ohne Prozentfeld. Ein ergänzender Live-Vergleich am 27. November 2026 mit dem bestehenden API-Client ergab für `Softwareentwickler` bei 100 % 26 beziehungsweise 579 und bei 50 % 83 beziehungsweise 636 gemeldete Treffer; die jeweils erste Seite mit `nv_true` enthielt sowohl Stellen nach Vereinbarung ohne Prozentfeld als auch Stellen mit dem gewählten Prozentanteil. Dies sind Stichproben, keine Stabilitäts- oder Vollständigkeitszusage.

Die direkte Kombination im API-Parameter wird verwendet. Eine zusätzliche Suche mit lokaler Filterung und eine Prüfung mittels Detailabrufen sind angesichts dieses Backend-Verhaltens unnötig und würden zusätzliche Anfragen sowie Probleme mit Seitengrenzen verursachen. Die Community-Dokumentation beschreibt den Parameter nicht; seine Semantik kann sich ändern.

## Verhalten

Die Option `--homeoffice-ohne-prozent` mit den Werten `einbeziehen` und `ausschliessen` setzt `--homeoffice` voraus. Bei `einbeziehen` wird an den vorhandenen API-Wert `;nv_true` angehängt. Bei `ausschliessen` wird der bestehende Prozentwert ohne Zusatz gesendet. Ohne neue Option bleibt das bestehende Verhalten unverändert. Die Option erscheint lesbar in `query`; die JSON-Hülle und `schema_version` bleiben erhalten. Alle Suchkombinationen erhalten denselben Parameter; Paginierung, Deduplizierung und Sortierung bleiben unverändert. Angaben nach Vereinbarung belegen keinen konkreten Homeoffice-Anteil; Details und Stellenbeschreibung bleiben zu prüfen.

## Prüfung

Netzwerkfreie Tests prüfen beide Wahlmöglichkeiten, ungültige Kombinationen und Werte, alle bisherigen Prozentwerte, kombinierte Suchen, den API-Transport sowie die lesbare Ausgabe und unverändertes Standardverhalten. Ein begrenzter Live-Vergleich und die Dokumentation der beobachteten Wirkung und Grenzen ergänzen die regulären Tests. CLI-Hilfe, Skill und Nutzungsdokumentation beschreiben die Option.
