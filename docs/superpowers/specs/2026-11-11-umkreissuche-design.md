# Umkreissuche

Ziel ist die optionale Angabe `--wo Ort:Kilometer`. Ohne Doppelpunkt bleibt der Ort unverändert; ohne `--wo` wird kein Ort gesendet. Der CLI-Eingang zerlegt die Angabe und sendet `wo` und `umkreis` getrennt; die Ausgabe `query` zeigt die gesendeten Werte. Ungültige Angaben führen vor einem Netzaufruf zu einem Eingabefehler.

Als Alternative wäre ein eigener CLI-Schalter möglich, der aber die im Issue gewünschte Schreibweise nicht erfüllt. Eine unveränderte Weitergabe des gesamten Werts würde den API-Parameter nicht setzen. Der Client akzeptiert vorsorglich ganzzahlige Kilometer von 0 bis 200; die BA-Hilfe beschreibt bis 200 km für ihre Oberfläche, nicht verbindlich für die inoffiziell dokumentierte API. Änderungen an der API bleiben möglich. Die Suchlogik und Laufzeitabhängigkeiten bleiben unverändert.
