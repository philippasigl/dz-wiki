# Review-Queue

Diese Datei wird von **`/wiki-auto-update`** bei jedem Lauf neu geschrieben und dient
gleichzeitig als Body des Draft-PR. Sie listet pro neuer Publikation genau die Punkte, die
ein Mensch bestätigen muss, bevor der PR gemergt wird (Merge = live):

- **Cluster** — bei Grenzfällen gewählte ID + plausibelste Alternative
- **Kanten** — vorgeschlagene Graph-Edges (außer `confidence: hoch`) zum Bestätigen/Verwerfen
- **Fact-Check** — `⚠`/`✗`-Findings aus `wiki/_fact-check/<slug>.md`
- **ignore: yes?** — Übersetzungs-/Duplikat-Kandidaten
- **Hub-Folgearbeit** — Themen, die vermutlich ein `/auto-wiki update-all` brauchen

Noch kein automatischer Lauf erfolgt. Nach dem ersten `/wiki-auto-update` steht hier die
konkrete Queue.
