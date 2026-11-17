# Filter für das Veröffentlichungsalter

Issue #20 ergänzt eine optionale Suche nach dem Veröffentlichungsalter. Ein ganzzahliger Tageswert von 0 bis 100 wird als `--veroeffentlichtseit` angenommen, in `query` ausgewiesen und bei jeder Einzelsuche als gleichnamiger API-Parameter übergeben. Ohne Option bleibt das Verhalten unverändert. Ungültige Eingaben führen vor jeder Anfrage zu einem Fehler.

Die direkte Übergabe nutzt den dokumentierten API-Filter und erhält die bestehende Seitennavigation. Eine nachträgliche Auswertung einzelner Stellendetails wäre aufwendiger und könnte die Vollständigkeit der Ergebnisse verändern. Die Bedeutung der API-Angabe und der Wertebereich sind nicht verbindlich garantiert; begrenzte Live-Vergleiche und ihre Grenzen werden dokumentiert. Netzwerkfreie Tests prüfen Randwerte, Fehler, Ausgabe und kombinierte Suchen. Das externe Ausgabeformat bleibt kompatibel; die Skill-Version steigt auf 1.1.0.
