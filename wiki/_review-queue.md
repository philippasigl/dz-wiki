# Review-Queue — Auto-Update 2026-06-11

Automatischer Lauf hat **3 neue Publikationen** entworfen und **1 Duplikat** markiert. Bitte je
Paper die offenen Punkte prüfen, ggf. im Stub korrigieren, dann den PR mergen (Merge = live).

Branch: `auto/wiki-update-2026-06-11`

Alle Stubs bestehen `check_stub_format.py` ([OK]) und `check_stub_numbers.py` (0 fehlende Zahlen).
Der Lauf übernimmt auch die Restarbeit des unterbrochenen Laufs vom 2026-06-01 (2 PDFs aus Backlog).

> **Review 2026-06-11 (Philippa):** Kante viel-wissen-wenig-wachstum → intel-magdeburg-analyse-de
> **verworfen** (aus dem Graphen entfernt); alle übrigen Punkte bestätigt.

## viel-wissen-wenig-wachstum  ([wiki/publikationen/viel-wissen-wenig-wachstum.md](wiki/publikationen/viel-wissen-wenig-wachstum.md))
„Viel Wissen, wenig Wachstum" — Innovationsförderung des Bundes, 2026-05-28, Wangenheim/Marx/Schuster-Johnson.
- **Cluster:** `wirtschaftspolitik` — Grenzfall? Alternative: `haushalt` (Allokation der 23 Mrd. € FuE-Bundesausgaben); Fokus liegt aber auf Unternehmensförderung/Innovationspolitik.  ☑ ok
- **Kanten:**
  - → `comeback-deutschland-industrie-turnarounds` (hoch, explizite Referenz Paleschke 2026)  ☑ ok
  - → `wie-viel-bang-for-the-buck-steckt-in-subventionen` (**mittel**, thematisch, keine Zitation)  ☑ bestätigt
  - ~~→ `intel-magdeburg-analyse-de` (niedrig)~~  ☑ **verworfen** — aus dem Graphen entfernt (Review 2026-06-11)
- **Fact-Check:** 0 ✗ / 1 ⚠ — Schlussfolgerungs-Verweis auf [[wie-viel-bang-for-the-buck-steckt-in-subventionen]] ist redaktionelle Einordnung, im PDF nicht zitiert. Hinweis: PDF selbst inkonsistent beim Großunternehmen-Anteil (S. 10: 65 %, S. 16: 64 %); Stub folgt 65 %. Siehe `wiki/_fact-check/viel-wissen-wenig-wachstum.md`  ☑ geprüft
- **ignore: yes?** nein — eigenständige Publikation  ☑ ok
- **Hub-Folgearbeit:** ggf. `/auto-wiki update-all` für Thema `wirtschaft` (Industriepolitik/Subventionen)

## planungssicherheit-fuer-die-schiene  ([wiki/publikationen/planungssicherheit-fuer-die-schiene.md](wiki/publikationen/planungssicherheit-fuer-die-schiene.md))
„Planungssicherheit für die Schiene: Was Deutschland von Österreich und der Schweiz lernen kann", 2026-06-01, Huwe/Illenseer.
- **Cluster:** `infra` — Grenzfall! Alternative: `haushalt`. Begründung infra: Kern ist Finanzierungsstruktur außerhalb des Bundeshaushalts (Sondervermögen + schuldenbremsenneutrale Annuitätenfinanzierung). Aber: die Schwester-Papiere `entgleist` und `eckpunkte-...verkehrssystems` liegen in `haushalt` — falls Konsistenz wichtiger ist, umhängen.  ☑ ok (bleibt infra)
- **Kanten** (alle hoch, explizit zitiert):
  - → `bahn-strassen-finanzieren-ohne-schuldenbremse` (Schuster et al. 2024)  ☑ ok
  - → `eckpunkte-fuer-die-finanzierung-eines-zukunftsfaehigen-verkehrssystems` (Agora/DZ 2025)  ☑ ok
  - → `entgleist` (Huwe & Illenseer 2025)  ☑ ok
  - *Nicht angelegt:* → `bundeshaushaltsmonitor-2026` (zwar zitiert, aber geringe thematische Nähe)  ☑ ok (nicht angelegt)
- **Fact-Check:** 0 ✗ / 2 ⚠ — (1) Maut-Kennzahl „10 Mrd. € 2035" lässt PDF-Bedingung „sofern etwa hälftig der Schiene bereitgestellt" weg; (2) Trassenpreis-Zuschreibung an [[entgleist]] — PDF zitiert tatsächlich Huwe & Illenseer 2025 „Warum Bahnfahren noch teurer wird" (inhaltlich deckungsgleich). Siehe `wiki/_fact-check/planungssicherheit-fuer-die-schiene.md`  ☑ geprüft
- **ignore: yes?** nein  ☑ ok
- **Hub-Folgearbeit:** `/auto-wiki update-all` für Thema `verkehr` empfohlen (drittes Schienen-Paper)

## welche-maerkte-sich-lohnen  ([wiki/publikationen/welche-maerkte-sich-lohnen.md](wiki/publikationen/welche-maerkte-sich-lohnen.md))
„Welche Märkte sich lohnen" — Tragfähigkeitscheck für wirtschaftspolitische Hebel, 2026-06-09, Görlich/Paleschke.
- **Cluster:** `wirtschaftspolitik` — Grenzfall? Alternative: `haushalt` (Subventionen/Finanzhilfen aus dem Bundeshaushalt); Kern ist aber Bewertung privater Geschäftsmodelle.  ☑ ok
- **Kanten:**
  - → `comeback-deutschland-industrie-turnarounds` (hoch, Paleschke 2026)  ☑ ok
  - → `wie-viel-bang-for-the-buck-steckt-in-subventionen` (hoch, Schuster-Johnson & Sigl-Glöckner 2026)  ☑ ok
  - → `bundeshaushaltsmonitor-2026` (hoch, 28-Mrd.-Referenz)  ☑ ok
  - → `wie-china-markt-fuer-markt-erobert` (**mittel**, China-Schock-2.0-Anschluss ohne Zitation)  ☑ bestätigt
- **Fact-Check:** 0 ✗ / 1 ⚠ — PDF-Deckblatt sagt „Hintergrundpapier", Frontmatter `policy-paper` (entspricht bestehender Konvention, Schema kennt kein `hintergrundpapier`). Siehe `wiki/_fact-check/welche-maerkte-sich-lohnen.md`  ☑ geprüft
- **ignore: yes?** nein  ☑ ok
- **Hub-Folgearbeit:** zusammen mit viel-wissen-wenig-wachstum → Thema `wirtschaft`

## kapitalbedarfe-und-finanzierung-von-energieverteilnetzen (Duplikat)
- PDF ist **byte-identisch** (4 225 379 Bytes) mit `Investitionen in eine zukunftsfähige Daseins­vorsorge.pdf` — der Website-Artikel „Kapitalbedarfe und Finanzierung von Energieverteilnetzen" verlinkt dieselbe Agora/Stiftung-Klimaneutralität/DZ-Analyse.
- Stub mit `ignore: yes` angelegt, Hauptknoten bleibt [[investitionen-in-eine-zukunftsfaehige-daseinsvorsorge]]. Kein Graph-Node.  ☑ ok

## Fehlgeschlagen / manuell
- keine — alle 4 PDFs der Arbeitsliste verarbeitet.

## Nicht in diesem Lauf genommen (Backlog über --max hinaus)
- keine.
