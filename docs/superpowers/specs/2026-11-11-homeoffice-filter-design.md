# Entwurf: Homeoffice-Filter und Live-Integrationstests

## Ziel und Rahmen

Issue #12 behebt den Homeoffice-Filter und ergänzt getrennt ausführbare Integrationstests gegen die reale BA-API. Die Laufzeit verwendet weiterhin ausschließlich die Python-Standardbibliothek. Die reguläre Testsuite benötigt kein Netzwerk; API-Angaben bleiben externe, veränderliche Daten.

## Alternativen und Entscheidung

Die vorhandene CLI übersetzt den optionalen Prozentwert direkt in den API-Parameter `homeoffice`. Eine zusätzliche Filterung über Stellendetails würde zahlreiche Anfragen erfordern und die Paginierung verändern; sie ist für die angeforderte Abfrage nicht nötig. Ein reiner Transporttest würde das Zusammenspiel von CLI, Suche und Detailabruf nicht prüfen. Daher verwenden die Live-Tests die bestehende CLI und rufen eine begrenzte Anzahl Details ab.

## Verhalten

Ohne `--homeoffice` wird kein Homeoffice-Filter gesendet. `--homeoffice` ohne Wert entspricht `100%`; als explizite Werte sind ausschließlich `0%`, `25%`, `50%` und `100%` zulässig. Sie ergeben `homeoffice=prozentual_0`, `prozentual_25`, `prozentual_50` beziehungsweise `prozentual_100`. Andere Eingaben erzeugen den bestehenden JSON-Eingabefehler. Die Ausgabehülle bleibt unverändert; `query.homeoffice` zeigt den verständlichen Prozentwert.

Die BA-Semantik ist nicht verbindlich dokumentiert. Stichproben am 11. November 2026 lieferten für die vier Werte unterschiedliche Trefferzahlen und in Details Felder `homeofficemoeglich`, `homeofficetyp` und `homeofficeprozent`. Diese Beobachtung belegt keine Vollständigkeit oder Garantie für jede Stellenangabe; Nutzende prüfen Stellenbeschreibungen und Bedingungen selbst.

## Prüfung

Netzwerkfreie Tests decken Abwesenheit, Standard, alle zulässigen Werte, ungültige Werte und den gesendeten Parameter ab. Die gesondert und ausdrücklich aufgerufenen Integrationstests führen eine ungefilterte Suche mit anschließendem Detailabruf sowie eine Homeoffice-Suche mit begrenzter Stichprobe von Detailabrufen aus. Die Homeoffice-Prüfung erwartet geeignete strukturierte Angaben in den Details und meldet fehlende oder widersprüchliche Angaben als Testfehler; externe Änderungen, leere Ergebnisse oder Dienststörungen sind anhand der Fehlermeldung zu untersuchen, nicht als Erfolg zu behandeln. Anzahl der Anfragen und Aufruf werden dokumentiert. Coverage und Ruff gelten für die reguläre Suite.
