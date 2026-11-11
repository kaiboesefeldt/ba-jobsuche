# GitHub-Zugriff für die Entwicklung

Für dieses Repository erfolgt der GitHub-Zugriff als GitHub App `kai-codex-agent`, nicht über Kais persönliches GitHub-Konto. Die App ist für `kaiboesefeldt/ba-jobsuche` installiert. Das gilt auch für künftige Sessions; die GitHub CLI ist nicht erforderlich.

## Lokale Einrichtung

- App-ID: `5708654`
- Installations-ID: `180787526`
- Bot-Identität für lokal erstellte Commits: `kai-codex-agent[bot]` und `355223922+kai-codex-agent[bot]@users.noreply.github.com`
- Privater Schlüssel auf diesem Rechner: `~/.config/kai-codex-agent/private-key.pem`

IDs, Berechtigungen und Installationsumfang können sich ändern. Der Schlüssel bleibt außerhalb des Repositorys und darf weder ausgegeben noch eingecheckt oder an Dritte übertragen werden. Zugriff auf ihn nur zur Authentifizierung verwenden. Fehlt er oder ist die App nicht erreichbar, den Nutzer informieren; nicht auf sein persönliches Konto ausweichen.

## Authentifizierung und Aufrufe

Das Entwicklungsskript `scripts/github_app.py` benötigt Python, OpenSSL und Netzwerkzugriff. Für Git-Befehle ist zusätzlich Git erforderlich. Es erzeugt ein App-JWT und ein kurzlebiges Installationstoken und greift direkt auf die GitHub-API zu oder startet Git mit der App-Identität:

```bash
python3 scripts/github_app.py api /repos/kaiboesefeldt/ba-jobsuche
python3 scripts/github_app.py api '/repos/kaiboesefeldt/ba-jobsuche/pulls?state=open'
python3 scripts/github_app.py api --method POST --input /tmp/pr.json /repos/kaiboesefeldt/ba-jobsuche/pulls
python3 scripts/github_app.py git push origin <branch>
```

App-ID, Installations-ID und Schlüsselpfad lassen sich über `--app-id`, `--installation-id` und `--key` oder die Umgebungsvariablen `GITHUB_APP_ID`, `GITHUB_APP_INSTALLATION_ID` und `GITHUB_APP_KEY` überschreiben. Die allgemeinen Optionen stehen vor `api` beziehungsweise `git`. Bei API-Aufrufen kann ein JSON-Body aus einer Datei übergeben werden. `python3 scripts/github_app.py --help` und `python3 scripts/github_app.py api --help` zeigen die Details.

API-Aufrufe gehen ausschließlich an `api.github.com`; Weiterleitungen werden abgelehnt. Für Git wird das Token als flüchtige, auf `https://github.com/` begrenzte HTTP-Konfiguration im Kindprozess übergeben. Es wird nicht als Kommandozeilenargument übergeben oder dauerhaft gespeichert. Umgebungsvariablen können jedoch für berechtigte Prozesse auf demselben System sichtbar sein; nur vertrauenswürdige Befehle aufrufen und keine Debug-Ausgaben aktivieren, die Zugangsdaten offenlegen. Nur HTTPS-Remotes auf GitHub verwenden; SSH nutzt diese Authentifizierung nicht.

Die regulären Tests laufen ohne Netzwerk und Schlüssel: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`. Ein Live-Aufruf prüft zusätzlich die App-Installation, aber ist kein Ersatz für die Tests.

Für die Entwicklung ist Ruff in `requirements-dev.txt` festgelegt. Nach Installation in einer virtuellen Umgebung prüfen `ruff check scripts tests` und `ruff format --check scripts tests` den Code. Ruff ist keine Laufzeitabhängigkeit des Skripts.

JWT und Installationstoken weder ausgeben noch dauerhaft in Git-Konfiguration, Dateien, Shell-Historie, URLs oder Commit-Nachrichten speichern. Keine Zugangsdaten in Tool-Ausgaben oder PRs aufnehmen. Die App-Authentifizierung ersetzt keine Zustimmung zu Aktionen, die eine solche benötigen.

## Arbeitsablauf und Prüfung

Vor einem Schreibzugriff Repository, Branch und aktuelle Änderungen prüfen. Auf Arbeitsbranches committen und pushen; Pull Requests als App erstellen. Der Nutzer prüft und merged. Bei lokal erstellten Commits die Bot-Identität ausdrücklich für den jeweiligen Commit setzen und den in `AGENTS.md` vereinbarten Trailer ergänzen; ein App-Push allein ändert die Git-Autorenschaft nicht.

Die eingeräumten App-Rechte und die Autorenschaft eines PRs bei Bedarf über die API prüfen. Fehlende Berechtigungen oder eine noch ausstehende Bestätigung der Installation melden, statt größere Rechte vorauszusetzen. Branch-Schutz nicht als aktiv annehmen: Bei der Einrichtung dieses privaten Repositorys war `main` nicht geschützt.
