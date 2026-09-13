# Review-Queue — Auto-Update 2026-09-10

Automatischer Lauf hat **2 neue Publikationen** entworfen. Bitte je Paper die offenen Punkte
prüfen, ggf. im Stub korrigieren, dann den PR mergen (Merge = live).

Branch: `auto/wiki-update-2026-08-27` (Lauf vom 27.08. war beim Download stehengeblieben und
wurde hier fortgeführt, statt einen neuen Branch aufzumachen)

## china-s-dedollarisation-strategy ([wiki/publikationen/china-s-dedollarisation-strategy.md](wiki/publikationen/china-s-dedollarisation-strategy.md))

Nils Gerresheim, Max Krahé, Jens van 't Klooster · 2026-07-07 · Policy Paper

- **Cluster:** `geldpolitik und anleihemärkte` — Grenzfall. Alternative: `ausland`. Gewählt wie
  beim Vorgängerpapier desselben Autorentrios (`die-folgen-einer-euro-internationalisierung`);
  das Papier behandelt Währungsinternationalisierung, nicht Außenbeziehungen als solche.  ☐ ok
- **Kanten:**
  - `china-s-dedollarisation-strategy → die-folgen-einer-euro-internationalisierung`
    (hoch, „Wohlfahrtsschätzung Euro-Internationalisierung") — im Literaturverzeichnis belegt.  ☐ bestätigen ☐ verwerfen
  - `china-s-dedollarisation-strategy → europas-truempfe-gegen-trump`
    (hoch, „Dollarabhängigkeit als Druckmittel") — Sigl-Glöckner (2026) im Literaturverzeichnis.
    Zeigt auf den deutschen Hauptknoten, weil `europe-s-trump-cards` `ignore: yes` trägt.  ☐ bestätigen ☐ verwerfen
- **Fact-Check:** 0 ✗ / 2 ⚠ — `wiki/_fact-check/china-s-dedollarisation-strategy.md` (lokal, gitignored).
  Beide ⚠ unkritisch; #2 ist die korpusweite Frage „van 't Klooster" vs. „van’t Klooster".  ☐ geprüft
- **ignore: yes?** nein — eigenständige Publikation.  ☐ ok
- **Hub-Folgearbeit:** `/auto-wiki update-all` für Geldpolitik & Anleihemärkte (Euro-Internationalisierung,
  Dollarabhängigkeit) — der Hub kennt das Papier noch nicht.

## wie-andere-laender-die-rente-finanzieren ([wiki/publikationen/wie-andere-laender-die-rente-finanzieren.md](wiki/publikationen/wie-andere-laender-die-rente-finanzieren.md))

Saskia Gottschalk, Florian Schuster-Johnson, Hannah Hägele, Amelie Kaupa · 2026-06-22 · Policy Paper

- **Cluster:** `haushalt` — Grenzfall. Alternative: `makro`. Gewählt, weil die Zielgröße die
  Belastung des Bundeshaushalts durch Alterssicherung ist, nicht der Arbeitsmarkt.  ☐ ok
- **Kanten:**
  - `→ bundeshaushaltsmonitor-2026` (hoch, „Haushaltslücke als Ausgangslage") — im Literaturverzeichnis belegt.  ☐ bestätigen ☐ verwerfen
  - `→ 5-milliarden-spielraum-im-sozialstaat-gewinnen` (hoch, „Sozialstaatsausgaben-Vorarbeit") — belegt.  ☐ bestätigen ☐ verwerfen
  - `→ wer-reformen-will-muss-kitas-bauen` (mittel, „Erwerbstätigkeit und Haushaltswirkung") —
    Zitat belegt, aber der Zielknoten ist doppelt vorhanden (siehe Sammelpunkte unten).  ☐ bestätigen ☐ verwerfen
  - `→ was-kostet-eine-sichere-lebenswerte-und-nachhaltige-zukunft` (mittel, „Finanzbedarfe des Staates") —
    zitiert, aber nur als Hintergrund.  ☐ bestätigen ☐ verwerfen
- **Fact-Check:** 0 ✗ / 2 ⚠ — `wiki/_fact-check/wie-andere-laender-die-rente-finanzieren.md` (lokal, gitignored).
  ⚠ #1: „11 Mrd. €" steht im PDF ausgeschrieben („elf Milliarden Euro"); `check_stub_numbers.py`
  hat die Ziffernfolge nur andernorts gefunden, also falsch-positiv bestätigt. Inhaltlich korrekt.  ☐ geprüft
- **ignore: yes?** nein — eigenständige Publikation.  ☐ ok
- **Hub-Folgearbeit:** `/auto-wiki update-all` für Haushalt und ggf. einen Sozialstaat-/Rente-Hub —
  bisher existiert keine Themenseite zur Alterssicherung.

## Sammelpunkte (nicht paper-spezifisch)

- **Scraper lädt Duplikate — behoben.** `download_fachtexte.py` deduplizierte nur über den
  Dateinamen. Die Website liefert dieselbe PDF unter wechselnden Namen (Halbgeviertstrich vs.
  Bindestrich, gerades vs. typografisches Apostroph, Lang- vs. Kurztitel), deshalb kamen in
  diesem Lauf **12 byte-identische Duplikate** herunter. Alle 12 wurden gelöscht.
  Das Skript lädt jetzt in eine Temp-Datei, vergleicht den MD5 gegen einen Index aller
  vorhandenen PDFs und verwirft Treffer, bevor sie im Korpus landen; verworfene Dateien stehen
  in `download_log.json` unter `duplicates_removed`. Gegenprobe: erneuter Lauf meldet
  0 Downloads, 12 Duplikate, 0 Fehler, PDF-Zahl unverändert 119.  ☐ ok
- **`add_to_graph.py` war veraltet — behoben.** Es schrieb `cluster` statt `clusterA`/`clusterB`,
  ließ `pdf_url`/`web_url`/`summary` weg und kannte den Cluster `geldpolitik und anleihemärkte`
  nicht (brach dort ab). Die beiden Nodes dieses Laufs wurden deshalb von Hand im Bestandsformat
  eingetragen. Das Skript schreibt jetzt das Bestandsformat; `clusterA` kann optional im
  Frontmatter gesetzt werden und fällt sonst auf die Cluster-ID zurück. Gegenprobe: das Skript
  erzeugt für `china-s-dedollarisation-strategy` exakt den von Hand eingetragenen Knoten.  ☐ ok
- **Doppelter Knoten für dieselbe Publikation:** `reformen-brauchen-kitas` und
  `wer-reformen-will-muss-kitas-bauen` beschreiben „Wer Reformen will, muss Kitas bauen", keiner
  trägt `ignore: yes`. Vorbestehend, nicht aus diesem Lauf.  ☐ Hauptknoten festlegen
- **`markitdown` nicht im PATH.** `convert_pdf_to_markdown.py` ruft das CLI auf; unter Windows
  liegt es in `…\Python311\Scripts`, das nicht im PATH ist — die Konvertierung meldet dann
  fälschlich „markitdown nicht installiert". Im Lauf per PATH-Erweiterung umgangen, Skript
  unverändert.  ☐ Aufruf auf `python -m` umstellen?
- **`--reviewer` im Skill wirkungslos.** `gh pr create --reviewer philippasigl` läuft ins Leere,
  weil GitHub keine Review-Anfrage an die Autorin des PRs zulässt (`reviewRequests` bleibt leer).
  Die Benachrichtigungs-Mail, auf die der `wiki-auto-update`-Skill baut, kommt damit nie.  ☐ Skill anpassen?
- **`web_url`-Konvention hat sich geändert.** Die Website nutzt jetzt
  `dezernatzukunft.org/publikationen/<slug>` (per `<link rel="canonical">` bestätigt); der
  Bestand hat überwiegend die alte Form `dezernatzukunft.org/<slug>/`. Die beiden neuen Stubs
  nutzen die neue Form.  ☐ Bestand später angleichen?

## Fehlgeschlagen / manuell

- keine

## Nicht in diesem Lauf genommen (Backlog über --max hinaus)

- keine — `needs_reprocessing.py` ist nach dem Lauf leer
