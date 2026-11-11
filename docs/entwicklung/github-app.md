# GitHub-Zugriff für die Entwicklung

Für dieses Repository erfolgt der GitHub-Zugriff als GitHub App `kai-codex-agent`, nicht über Kais persönliches GitHub-Konto. Die App ist für `kaiboesefeldt/ba-jobsuche` installiert. Das gilt auch für künftige Sessions; `gh auth login` mit dem persönlichen Konto ist dafür nicht erforderlich.

## Lokale Einrichtung

- App-ID: `5708654`
- Installations-ID: `180787526`
- Bot-Identität für lokal erstellte Commits: `kai-codex-agent[bot]` und `355223922+kai-codex-agent[bot]@users.noreply.github.com`
- Privater Schlüssel auf diesem Rechner: `~/.config/kai-codex-agent/private-key.pem`

IDs, Berechtigungen und Installationsumfang können sich ändern. Der Schlüssel bleibt außerhalb des Repositorys und darf weder ausgegeben noch eingecheckt oder an Dritte übertragen werden. Zugriff auf ihn nur zur Authentifizierung verwenden. Fehlt er oder ist die App nicht erreichbar, den Nutzer informieren; nicht auf sein persönliches Konto ausweichen.

## Authentifizierung und Aufrufe

1. Mit dem privaten Schlüssel ein kurzlebiges, mit RS256 signiertes App-JWT erzeugen. Für `iss` die App-ID verwenden und `iat` sowie `exp` entsprechend den [GitHub-Vorgaben](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app) setzen; beispielsweise lässt sich `openssl` zum Signieren verwenden.
2. Das JWT ausschließlich zur Authentifizierung von `POST /app/installations/180787526/access_tokens` verwenden. Das zurückgegebene Installationstoken gilt nur begrenzt und erhält höchstens die Rechte der Installation. Bei Bedarf die [GitHub-Dokumentation zum Installationstoken](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app) beachten.
3. GitHub-API-Anfragen mit dem Installationstoken als Bearer-Token ausführen. Alternativ kann `gh` das Token für einen einzelnen Prozess über `GH_TOKEN` erhalten. Für Git über HTTPS das Token nur flüchtig als Zugangsdaten übergeben und nur mit `github.com` verwenden.

JWT und Installationstoken weder ausgeben noch in Git-Konfiguration, Dateien, Shell-Historie, URLs oder Commit-Nachrichten speichern. Keine Zugangsdaten in Tool-Ausgaben oder PRs aufnehmen. `~/.config` und `/tmp` sind keine Ersatzorte für dauerhaft gespeicherte Tokens. Die App-Authentifizierung ersetzt keine Zustimmung zu Aktionen, die eine solche benötigen.

## Arbeitsablauf und Prüfung

Vor einem Schreibzugriff Repository, Branch und aktuelle Änderungen prüfen. Auf Arbeitsbranches committen und pushen; Pull Requests als App erstellen. Der Nutzer prüft und merged. Bei lokal erstellten Commits die Bot-Identität ausdrücklich für den jeweiligen Commit setzen und den in `AGENTS.md` vereinbarten Trailer ergänzen; ein App-Push allein ändert die Git-Autorenschaft nicht.

Die eingeräumten App-Rechte und die Autorenschaft eines PRs bei Bedarf über die API prüfen. Fehlende Berechtigungen oder eine noch ausstehende Bestätigung der Installation melden, statt größere Rechte vorauszusetzen. Branch-Schutz nicht als aktiv annehmen: Bei der Einrichtung dieses privaten Repositorys war `main` nicht geschützt.
