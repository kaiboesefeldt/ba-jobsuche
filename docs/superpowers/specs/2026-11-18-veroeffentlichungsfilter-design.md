# Veröffentlichungsfilter und Sortierung

## Ziel und Rahmen

Issue #24 behebt die irreführende direkte Übergabe beliebiger Tageswerte und ordnet Suchergebnisse nach Erstveröffentlichung. Die CLI bleibt bei Eingaben von 0 bis 100 Tagen; die Ausgabe zeigt den gewünschten Wert, nicht die technische Vorauswahl. Die API und ihre Daten können sich ändern; einzelne Live-Stichproben begründen keine Vollständigkeitsgarantie.

## Ansätze

Eine ausschließlich lokale Sortierung ordnet abgerufene Treffer zuverlässig, beeinflusst aber nicht, welche Treffer bei einer Seitengrenze abgerufen werden. Zusätzlich `sort=veroeffdatum` anzufordern verbessert nach bisherigen Beobachtungen diese Auswahl; die anschließende lokale Sortierung sorgt auch bei kombinierten Suchen für eine gemeinsame Reihenfolge. Diese Kombination wird vorgeschlagen. Ein frühzeitiger Seitenabbruch anhand des Datums wird mangels belastbarer Garantie nicht eingeführt.

## Verhalten

Für 0 bis 28 Tage dient die nächstgrößere empirisch beobachtete API-Stufe aus 0, 1, 7, 14 und 28 als Vorauswahl. Für größere Werte wird kein API-Zeitfilter gesendet. Nach Abruf und Deduplizierung wird lokal nach `datumErsteVeroeffentlichung` gefiltert: maßgeblich ist das lokale Kalenderdatum des ausführenden Systems zum Beginn der Suche, einschließlich des Grenztags. Fehlende oder ungültige Datumswerte bleiben enthalten und werden am Ende einsortiert; ihre Zahl wird auf stderr als Warnung ausgewiesen; die JSON-Hülle bleibt unverändert. Ohne Zeitfilter wird ebenfalls sortiert. Gültige Daten stehen absteigend, Gleichstände behalten ihre ursprüngliche Reihenfolge. Der aktuelle Veröffentlichungszeitraum wird nicht ersatzweise verwendet.

Die Seitennavigation und ihre Abbruchgründe bleiben unverändert. `complete` beschreibt weiterhin nur das reguläre Ende aller Einzelsuchen und ist keine Garantie für vollständige oder unveränderte Daten. API-Vorauswahl und Sortierparameter sind empirische Annahmen; die Vorauswahl kann bei geänderter API-Semantik Treffer ausschließen. Diese Grenze wird dokumentiert. Der Ausgabevertrag und die Versionsregeln werden bei der Implementierung anhand der bestehenden Release-Vorgaben geprüft.

## Prüfung

Netzwerkfreie Tests decken Grenztage, ungültige und fehlende Daten, Gleichstände, unterschiedliche Datumsfelder, kombinierte Suchen, Seitengrenzen und API-Parameter ab. Begrenzte gesonderte Live-Vergleiche prüfen Filterstufen und Sortierung über mehrere Seiten, ohne aus Stichproben eine Garantie abzuleiten. Nutzung, Skill, Schema und Release-Hinweise werden an das tatsächliche Verhalten angepasst.
