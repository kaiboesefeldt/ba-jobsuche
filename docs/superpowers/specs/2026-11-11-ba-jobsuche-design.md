# Entwurf: BA-Jobsuche-Skill (Issue #3)

## Ziel und Grenzen

Eine deutschsprachige Agent-Skill unterstützt persönliche Stellenrecherchen durch eine lokale CLI. Sie unterscheidet belegte Suchergebnisse von Bewertungen, nennt Quelle, Abrufzeit und Grenzen und bewirbt sich nicht. Suchbegriffe und Filter stammen vom Nutzer; personenbezogene Daten und Bewerbungsunterlagen gehören nicht in Anfragen. Verfügbarkeit und Vollständigkeit der Stellenangebote sind nicht garantiert.

## Zugangs- und Datenrechte

Die [BA-Nutzungsbedingungen](https://www.arbeitsagentur.de/nutzungsbedingungen) regeln unter anderem die Nutzung veröffentlichter Angebote und gesondert deren Veröffentlichung auf Drittplattformen. Die [Community-Dokumentation](https://github.com/bundesAPI/jobsuche-api) beschreibt einen technischen Zugriff, ist aber weder eine Autorisierung noch eine Stabilitätszusage. Eine ausdrückliche Freigabe der BA für den automatisierten Zugriff ist anhand dieser Quellen nicht festgestellt. Die Dokumentation nennt die Quellen und die Verantwortung der Nutzenden, die Bedingungen ihres jeweiligen Einsatzes zu erfüllen. Die Skill entscheidet nicht über die rechtliche Zulässigkeit.

## Gewählter Ansatz

Die Skill fragt die inoffizielle API direkt und ohne persönliche Anmeldung ab. Der von der Community dokumentierte öffentliche Kennwert `jobboerse-jobsuche` wird automatisch als `X-API-Key` gesendet; er ist kein persönlicher Schlüssel und keine Anmeldung. Da die API sich ändern kann, wird der Kennwert bei Bedarf austauschbar gehalten.

## Architektur und Schnittstellen

Python ab 3.10, ausschließlich Standardbibliothek zur Laufzeit. Ein API-Modul kapselt HTTPS, Timeout, Parameterkodierung, Status- und JSON-Fehler; ein Suchmodul validiert und normalisiert Antworten, begrenzt Seiten und erkennt fehlende oder widersprüchliche Daten. Eine CLI kapselt Argumente und Ausgabe. Der öffentliche API-Kennwert wird automatisch gesetzt. Die Suche ruft Seiten automatisch ab, entfernt Duplikate anhand der Referenznummer und meldet den Abbruchgrund. Standardmäßig sind höchstens zehn Seiten vorgesehen; die Clientgrenze kann über die CLI verändert werden. Keine automatischen Wiederholungen bei Sperren oder Ratenbegrenzung.

Die CLI bietet `search` mit explizitem Suchtext und optionalem Ort sowie `detail` mit Referenznummer. Eine versionierte JSON-Hülle enthält bei Erfolg `schema_version`, `ok`, `source`, `retrieved_at`, `query`, `results` und Hinweise zu Grenzen; bei Fehlern `schema_version`, `ok` und einen stabilen Fehlercode mit englischer Meldung. Ergebnisse enthalten externe Quellenfelder und keine Eignungsbewertung; fehlende Felder werden nicht erfunden. Fehler liefern einen von null verschiedenen Exit-Status und keine Zugangsdaten. Konkrete Felddefinitionen und Kompatibilitätsregeln sind im Implementierungsplan und der Nutzungsdokumentation festzulegen.

## Annahmen und Prüfung

Die Community beschreibt `/pc/v6/jobs`, die Parameter `was`, `wo`, `page`, `size`, den Header `X-API-Key` und einen Detailabruf mit kodierter Referenznummer. Formate, Seitennavigation, leere Ergebnisse und etwaige Grenzen sind gegen Quellen zu prüfen und als veränderliche Annahmen zu dokumentieren. Unerwartete Antworten dürfen nicht als vollständige Trefferliste ausgegeben werden. Leere Antwortformen sind nur dann als null Treffer zu behandeln, wenn sie dafür hinreichend belegt sind.

Netzwerkfreie Tests prüfen Parameter, Normalisierung, Pagination, Fehlerfälle, CLI-Vertrag und Schutz vor ungewollten Anfragen. Optionale Live-Prüfungen sind getrennt, ausdrücklich aktiviert und auf wenige Anfragen begrenzt; ihre Nutzung unterliegt den Bedingungen des jeweiligen Einsatzes. Ruff prüft und formatiert den Code. Die Skill erläutert Suchstrategie, Quellen und Bewertung getrennt; README und ausführliche Dokumentation beschreiben Installation, Voraussetzungen und Grenzen.

## Offene Punkte

- Die rechtlichen Bedingungen des jeweiligen Einsatzes sind von den Nutzenden zu beachten.
- Die API kann ihr Format und ihre Grenzen ändern; die Dokumentation hält die überprüften Annahmen fest.
