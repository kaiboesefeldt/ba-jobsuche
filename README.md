# BA-Jobsuche als Agent-Skill

Eine deutschsprachige Agent-Skill zur persönlichen Recherche von Stellenangeboten über die inoffizielle Schnittstelle der Bundesagentur für Arbeit. Python 3.10 oder neuer ist erforderlich; zur Laufzeit werden keine externen Bibliotheken benötigt.

```sh
python3 skills/ba-jobsuche/scripts/jobsuche.py search --was 'Softwareentwickler' --wo 'Berlin'
```

Zur Installation kannst du deinem Agenten sagen:

> Installiere die BA-Jobsuche-Skill aus https://github.com/kaiboesefeldt/ba-jobsuche und nutze die Installationsanleitung im Repository.

Die [Installationsanleitung für Agenten](docs/installation.md) beschreibt das Vorgehen und die Voraussetzungen.

Die [Skill](skills/ba-jobsuche/SKILL.md) beschreibt den Rechercheablauf; [Nutzung und Schnittstelle](docs/nutzung.md) erläutern Ausgabe, Seitennavigation, Tests und Grenzen. Die API ist inoffiziell dokumentiert und kann sich ändern. Nutzende sind für die Einhaltung der Bedingungen ihrer konkreten Nutzung verantwortlich.

Projektbeiträge stehen unter der [Apache License 2.0](LICENSE); für Dienst und Inhalte können gesonderte Bedingungen gelten.
