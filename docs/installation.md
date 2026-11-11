# Installation der BA-Jobsuche-Skill für Agenten

Diese Anleitung richtet sich an den Agenten, der die Skill im Auftrag einer Person installiert. Sie ist auch für Menschen lesbar. Quelle ist das Repository <https://github.com/kaiboesefeldt/ba-jobsuche>, Skill-Pfad `skills/ba-jobsuche/`. Das Verzeichnis enthält `SKILL.md`, `scripts/jobsuche.py`, das Python-Paket `scripts/ba_jobsuche/` und `references/`. Installiere das **ganze Verzeichnis**; die `SKILL.md` allein reicht nicht.

## Voraussetzungen und Vorgehen

1. Ermittle anhand des Auftrags und der Dokumentation deiner Agentenumgebung den Installationsort und den Geltungsbereich: projektbezogen im gewünschten Projekt oder persönlich für mehrere Projekte. Nutze einen vorhandenen, geeigneten Installationsmechanismus des Agenten bevorzugt. Wenn der Auftrag den Bereich nicht festlegt, berücksichtige den Kontext und teile den gewählten Bereich mit; bei entscheidender Unklarheit frage nach.
2. Der Agent benötigt Zugriff auf GitHub und Schreibrechte am Zielort. Für die Nutzung sind Python 3.10 oder neuer und Netzwerkzugriff auf die Jobsuche der Bundesagentur für Arbeit nötig. Prüfe die Version mit `python3 --version` beziehungsweise dem passenden Python-Aufruf der Umgebung. Zusätzliche Python-Pakete sind nicht nötig. Beachte die Berechtigungen und Sandbox-Regeln deiner Umgebung.
3. Installiere `skills/ba-jobsuche` mit der agenteneigenen Routine aus dem genannten Repository. Falls kein geeigneter Mechanismus verfügbar ist, beziehe das Repository und kopiere das vollständige Verzeichnis in den dokumentierten Skill-Ordner des gewählten Bereichs. Erhalte die Verzeichnisstruktur. Ein vorhandenes Ziel nicht ungeprüft überschreiben: vorhandene Installation und Nutzerauftrag prüfen und einen Konflikt gegebenenfalls mit der Person klären.
4. Prüfe die Dateien und den Skriptaufruf wie unten beschrieben. Starte, falls die Umgebung es verlangt oder die Skill nicht erkennt, eine neue Agentensitzung und prüfe die Erkennung dort. Teile Installationsort, Geltungsbereich, durchgeführte Prüfungen und verbleibende Einschränkungen mit.

### Beispiel für das Kopieren

Dies ist ein Shell-Beispiel für einen **neuen** Zielpfad; ersetze `<skill-ordner>` durch den für Agent und Geltungsbereich dokumentierten Ordner. Nutze einen temporären Checkout und beachte bei bestehenden Dateien Schritt 3. Andere Plattformen können gleichwertige Werkzeuge verwenden.

```sh
git clone https://github.com/kaiboesefeldt/ba-jobsuche.git /tmp/ba-jobsuche-install
mkdir -p '<skill-ordner>'
cp -R /tmp/ba-jobsuche-install/skills/ba-jobsuche '<skill-ordner>/ba-jobsuche'
```

Das Beispiel setzt voraus, dass weder `/tmp/ba-jobsuche-install` noch `<skill-ordner>/ba-jobsuche` existiert. Die Anführungszeichen entfernen oder den vollständigen konkreten Pfad darin einsetzen; ein wörtliches `~` innerhalb der Anführungszeichen wird von der Shell nicht expandiert. Für ein Update die vorhandene Installation und etwaige lokale Änderungen gesondert prüfen.

## Dokumentierte Orte für verbreitete Agenten

Die folgenden Beispiele sind aus den verlinkten offiziellen Dokumentationen abgeleitet (Stand: 11. November 2026). Projektpfade sind relativ zum jeweiligen Projekt; `~` bezeichnet das persönliche Benutzerverzeichnis in der Umgebung des Agenten. Entscheidend ist die Dokumentation der tatsächlich verwendeten Oberfläche und Version.

| Agent | Projektbezogen | Persönlich | Quelle und Hinweis |
| --- | --- | --- | --- |
| OpenAI Codex | `.agents/skills/ba-jobsuche/` | `~/.agents/skills/ba-jobsuche/` | [OpenAI: Installation](https://developers.openai.com/api/reference/cli); falls vorhanden, den Skill-Installer der Umgebung verwenden. |
| Claude Code | `.claude/skills/ba-jobsuche/` | `~/.claude/skills/ba-jobsuche/` | [Claude Code: Skills](https://code.claude.com/docs/en/skills) beschreibt weitere Geltungsbereiche und Prioritäten. |
| GitHub Copilot | `.github/skills/ba-jobsuche/` | `~/.copilot/skills/ba-jobsuche/` | [GitHub: Agent Skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills); unterstützte Orte hängen von der Oberfläche ab. |

Weitere Agenten: deren offizielle Dokumentation und gegebenenfalls eingebaute Installationsroutine verwenden. Kann die Umgebung keine kompatiblen Skills oder deren Skripte nutzen, die Einschränkung melden statt eine erfolgreiche Integration zu behaupten. Cloud- und lokale Umgebungen können unterschiedliche Dateisysteme und Berechtigungen haben.

## Installation prüfen und verwenden

Prüfe, dass im installierten Verzeichnis `SKILL.md`, `scripts/jobsuche.py`, `scripts/ba_jobsuche/__init__.py` und `references/output.schema.json` vorhanden sind. Führe das Skript über seinen tatsächlichen Pfad aus; es findet das benachbarte Python-Paket auch außerhalb des Repositorys. In den folgenden Beispielen `<installationspfad>` durch den absoluten Pfad zum installierten Verzeichnis ersetzen:

```sh
python3 '<installationspfad>/scripts/jobsuche.py' --help
python3 '<installationspfad>/scripts/jobsuche.py' search --help
```

Die relativen Aufrufe in `SKILL.md` setzen das Skill-Verzeichnis als Arbeitsverzeichnis voraus: Wechsle dafür dorthin oder verwende den absoluten Pfad zum Skript. Beide Hilfeaufrufe sind ohne Netzwerk möglich. Prüfe zusätzlich in einer neuen Agentensitzung, ob `ba-jobsuche` als Skill verfügbar ist, etwa über eine vorhandene Skill-Liste oder durch einen ausdrücklichen Aufruf nach den Regeln des Agenten. Sichtbarkeit und tatsächliche Verwendung sind getrennte Prüfungen. Ein Beispielauftrag lautet: „Suche mit der BA-Jobsuche-Skill nach Softwareentwicklungsstellen in Berlin.“ Prüfe dabei, ob der Agent das installierte Skript mit einem passenden Pfad tatsächlich ausführt. Eine echte Suche benötigt Netzwerkzugriff und kann abhängig vom Dienst fehlschlagen oder unvollständig sein.

Typische Fehler: Bei fehlendem Python oder falscher Version einen geeigneten Interpreter bereitstellen. Bei `ModuleNotFoundError` prüfen, ob `scripts/ba_jobsuche/` neben `jobsuche.py` vollständig kopiert wurde. Wird die Skill nicht erkannt, Ort, Geltungsbereich, Dateinamen und neue Sitzung prüfen. Bei Netzwerk- oder Berechtigungsfehlern die jeweilige Umgebung prüfen und den Fehler melden. Ein erfolgreicher `--help`-Aufruf belegt weder die Erkennung durch den Agenten noch den Zugriff auf die API.

Die Pfadangaben wurden anhand der Quellen geprüft; eine vollständige Installation und Nutzung mit jeder genannten Agentenumgebung ist dadurch nicht belegt. Die agentenübergreifende praktische Prüfung erfolgt gesondert.
