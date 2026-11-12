# Release-Versionierung und Updates (Issue #17)

## Ziel und Grenzen

Die vollständig gebündelte Skill erhält die erste stabile Version 1.0.0. Agenten aktualisieren sie ausschließlich auf ausdrücklichen Auftrag. Bei vermuteten API-Fehlern prüfen sie verfügbare stabile Releases und deren Hinweise und melden einen möglichen Zusammenhang, ohne selbst zu aktualisieren. Normale Suchanfragen lösen keine Versionsprüfung aus. Externe BA-Daten und die Verfügbarkeit des Dienstes sind nicht Teil einer Kompatibilitätszusage.

## Ansätze

Vereinbart sind GitHub-Releases mit SemVer und einer installierten Versionsangabe. Ein Git-Checkout für jede Installation würde den bestehenden Kopier- und Installer-Weg einschränken. Ein eigenes Updateprogramm würde zusätzliche Laufzeitlogik und agentenspezifische Annahmen einführen. Stattdessen beschreibt eine agentenlesbare Anleitung die Prüfung und Installation eines konkreten stabilen Releases; die Skill selbst verweist bei vermuteten API-Fehlern auf die Versionsprüfung.

## Version und Veröffentlichung

Eine Datei im Skill-Verzeichnis ist die einzige Quelle der Versionsnummer. Sie enthält eine stabile SemVer-Version ohne Präfix; das Git-Tag und der Release-Name verwenden `v` als Präfix. `schema_version` bleibt unabhängig. Versionshinweise werden im Repository gepflegt und dem zugehörigen Release zugeordnet; sie müssen API-Korrekturen und inkompatible Änderungen verständlich nennen.

Ein Pull-Request-Check prüft die Version gegen den aktuellen Zielbranch, akzeptiert beim ersten Release 1.0.0 und verlangt danach eine höhere stabile SemVer-Version. Ein Workflow für Pushes auf `main` prüft den jeweiligen Commit und seinen Vorgänger, erstellt das Tag und das stabile GitHub-Release und meldet ungültige Versionen, fehlende Hinweise und bereits vorhandene Tags oder Releases als Fehler. Der erste veröffentlichte Commit darf als Ausnahme einen Vorgänger ohne Versionsdatei haben. Das Tag muss auf den Commit des auslösenden Ereignisses zeigen; überlappende Läufe dürfen ältere Veröffentlichungen nicht abbrechen oder den fortgeschrittenen Branch-Head taggen. Für erfolgreiche Durchsetzung vor dem Merge muss der Check in den Repository-Regeln verpflichtend sein und auf einer aktuellen Zielbasis laufen; das bloße Vorhandensein des Workflows aktiviert keinen Branch-Schutz. Fehlgeschlagene Veröffentlichungen sind sichtbar und müssen nach Klärung gezielt wiederholt werden können, ohne einen anderen Commit zu taggen oder ein bestehendes Release still zu überschreiben. Veröffentlichung erfolgt nur nach tatsächlichem Merge, nicht während des Tests.

Ab 1.0.0 gelten Major für inkompatible Änderungen am dokumentierten öffentlichen Vertrag, Minor für kompatible Erweiterungen und Patch für kompatible Korrekturen. Jeder Merge erhöht die Version mindestens um einen Patch-Schritt. Bei parallelen PRs muss die Prüfung nach Aktualisierung der Zielbasis erneut stattfinden; konkurrierende Versionen werden vor dem Merge aufgelöst.

## Installation und Update

Erstinstallation und Update beziehen das vollständige Skill-Verzeichnis aus dem gewählten stabilen Release. Die Update-Anweisung ist auch innerhalb der installierten Skill auffindbar. Beim ausdrücklichen Update-Auftrag ermittelt der Agent Installationsort und installierte Version, vergleicht numerisch mit dem neuesten stabilen Release und ersetzt das Verzeichnis nur bei einer höheren Version. Er stellt das Verzeichnis des konkreten Tags vor dem Ersetzen vollständig bereit. Bei gleichem oder älterem Release meldet er, dass kein Update erfolgt. Bei unklaren Installationsorten fragt er nach; lokale Änderungen werden weder geprüft noch übernommen und beim Ersetzen überschrieben. Nach dem Update ist keine lokale Funktionsprüfung vorgeschrieben. Fehler bei Versionsabfrage oder Bereitstellung werden gemeldet und nicht als aktueller Stand ausgegeben.

## Öffentlicher Vertrag und Prüfungen

CLI-Befehle, Optionen, Exit- und Fehlercodes und die dokumentierte JSON-Ausgabehülle werden als öffentliche Schnittstelle erläutert. Die bereits verwendeten JSON-kodierten Zeichenketten für Mehrfachwerte bleiben zunächst erhalten, um bestehende Aufrufer nicht unnötig zu ändern; das nicht erzeugte `arbeitszeit`-Feld entfällt aus dem Schema. BA-Ergebnisfelder bleiben dynamisch. Die Entscheidung und ihre Auswirkungen sind in Schema, Tests und Dokumentation konsistent.

Netzwerkfreie Tests prüfen Versionsvergleich, Fehlerfälle, Workflow-Hilfslogik und bestehende CLI-Verträge. Tests, Coverage und Ruff werden ausgeführt. Die plattformübergreifende tatsächliche Erkennung und Nutzung der Skill wird, soweit die Umgebungen verfügbar sind, praktisch geprüft; nicht verfügbare Umgebungen werden als Einschränkung ausgewiesen. Release- und GitHub-Automation sind zusätzlich gegen ihre tatsächlichen Plattformbedingungen zu prüfen, ohne im Rahmen der Vorbereitung ein Release auszulösen.
