---
name: wiki-auto-update
description: >
  Automatischer Ende-zu-Ende-Lauf zur Aufnahme neuer DZ-Publikationen ins Wiki.
  Scraped dezernatzukunft.org nach neuen Fachtexten, konvertiert + entwirft jeden
  Stub vollständig, ergänzt Graph + Fact-Check, propagiert nach site/, schreibt
  eine Review-Queue und öffnet einen Draft-PR (kein Push auf main). Läuft alle
  zwei Wochen LOKAL (Windows-Aufgabe „DZ Wiki Auto-Update", interaktiv mit
  Bestätigung) oder manuell via /wiki-auto-update. NICHT als Remote-Routine — die
  Cloud ist von dezernatzukunft.org IP-blockiert (403); Scrape geht nur lokal.
  Verwende diesen Skill, wenn das Wiki turnusmäßig aktualisiert werden soll.
---

# DZ Wiki – Automatischer Update-Lauf

Bündelt den kompletten Ingestion-Workflow zu **einem** Lauf, der die mechanischen Schritte
selbst erledigt, jeden neuen Stub **bestmöglich vorausfüllt** und am Ende eine **Review-Queue**
übergibt — die offenen Urteilsfragen, die ein Mensch bestätigen muss. **Der Lauf publiziert nie
selbst:** er stagt alles auf einem Branch und öffnet einen **Draft-PR**. Mergen (= live gehen)
bleibt Handarbeit der Nutzerin.

Dieser Skill *orchestriert* die bestehenden Skills und Skripte — er erfindet keine Logik neu.
Für Detailregeln verweist er auf [pdf-ingestion](../pdf-ingestion/SKILL.md),
[network-maker](../network-maker/SKILL.md) und [fact-checker](../fact-checker/SKILL.md).

> **Lokal ausführen — nicht in der Cloud.** Der Scrape-Schritt (`download_fachtexte.py`) bekommt
> aus der Anthropic-Cloud `403 Forbidden` von dezernatzukunft.org (IP-/ASN-Sperre, kein
> User-Agent-Problem). Vom lokalen Rechner aus ist die Seite erreichbar. Deshalb läuft dieser
> Workflow per Windows-Aufgabe **„DZ Wiki Auto-Update"** alle zwei Wochen lokal — sie öffnet eine
> interaktive Claude-Session, vorbelegt mit `/wiki-auto-update`, via
> [scripts/run_wiki_update.cmd](../../../scripts/run_wiki_update.cmd). Ein Remote-Routine-Lauf
> findet nie neue Paper und no-opt.

## Aufruf

```
/wiki-auto-update
```

Optional `--max N` (Default: alle neuen). Mehr als ~8 neue Paper in einem Lauf ist
ungewöhnlich (Cadence ≈ 1 Paper/Woche); bei größerem Backlog `--max` setzen und den Rest im
Folgelauf nehmen — die Review-Queue listet den ungenommenen Rest.

## Drei Urteilsfragen, die NIE automatisch publiziert werden

Diese landen in der Review-Queue, nicht ungeprüft im Merge:

1. **Kernthesen / Schlussfolgerungen / Zahlen** — LLM-generiert, gegen das PDF zu prüfen.
2. **Cluster** bei Grenzfällen (siehe Entscheidungsbaum in [CLAUDE.md](../../../CLAUDE.md#themencluster-kanonisch)).
3. **Graph-Kanten** — jede nicht-triviale Edge braucht Bestätigung (network-maker-Regel).

## Was dieser Lauf bewusst NICHT tut

- **Themen-/Konzept-Hubs nicht auto-editieren.** Die DZ-Position über mehrere Paper zu
  synthetisieren ist zu urteilslastig für einen unbeaufsichtigten Lauf und würde kuratierte
  Seiten verwässern. Stattdessen listet die Review-Queue, welche Hubs vermutlich ein
  Folge-`/auto-wiki update-all` brauchen.
- **Kein `web-check`** im Cloud-Lauf (kein Chrome/MCP dort). Der Docusaurus-Build wird ohnehin
  vom Deploy-Action (`npm run build`) geprüft, sobald der PR gemergt ist.
- **Nicht auf `main` pushen, PR nicht mergen.** Nur Branch + Draft-PR.

## Robustheit

Einzelne Fehlschläge sind **nicht fatal**: Ein PDF, das die Konvertierung oder Validierung
nicht besteht, wird übersprungen und in der Review-Queue unter „Fehlgeschlagen / manuell“
gelistet — der Lauf bricht nicht ab.

## Workflow

### 0. Prep — sauberer Branch von aktuellem main

```bash
git checkout main && git pull
git checkout -b auto/wiki-update-<YYYY-MM-DD>
```

Abhängigkeiten sicherstellen (im Remote-Agent-Env evtl. nötig; lokal meist schon da):

```bash
pip install pyyaml jsonschema markitdown requests beautifulsoup4
```

Fällt `markitdown` aus (Cloud-Env ohne Wheel), den betroffenen PDF überspringen und in der
Review-Queue notieren — nicht den ganzen Lauf abbrechen.

### 1. Scrapen — was ist neu?

```bash
python scripts/download_fachtexte.py
```

Das Skript lädt nur **neue** PDFs (dedupe gegen `publikationen/`) und schreibt
`publikationen/download_log.json` neu. Die Liste der diesmal neu geladenen Dateien steht
danach unter dem Key `downloaded`:

```bash
python -c "import json; print('\n'.join(json.load(open('publikationen/download_log.json',encoding='utf-8'))['downloaded']))"
```

Das ist die **Arbeitsliste** dieses Laufs. Zur Sicherheit zusätzlich `needs_reprocessing.py`
laufen lassen — es fängt auch Backlog (PDFs ohne Stub-konformen Eintrag):

```bash
python scripts/needs_reprocessing.py --pdfs
```

Arbeitsliste = `downloaded` ∪ `needs_reprocessing` (auf `--max` begrenzen). Sind 0 neue Paper
da: trotzdem Schritt 9 (Review-Queue mit „keine neuen Publikationen“) und Schritt 11 nur, falls
es überhaupt einen Diff gibt — sonst ohne PR sauber beenden und das in der Schlussmeldung sagen.

### 2. Pro neuem PDF: Stub vollständig entwerfen

Pro Paper exakt dem [pdf-ingestion](../pdf-ingestion/SKILL.md)-Workflow folgen (dort liegen
alle Detailregeln: Zielformat, Format-Heuristik, Slug, `ignore: yes`, lange Paper):

```bash
python scripts/convert_pdf_to_markdown.py "publikationen/<datei>.pdf" wiki/publikationen/
# bei >15.000 Wörtern Rohkonvertierung zuerst:
python scripts/extract_long_paper_sections.py wiki/publikationen/<datei>.md
```

Dann **bestmöglich** ausfüllen: Frontmatter (title, date, authors, ggf. coauthors,
**best-guess cluster**, format nach Heuristik, tags), `## Kernthesen` (3–5),
`## Schlussfolgerungen` (mit `[[Links]]`), `## Zahlen`. Slug + Umbenennen:

```bash
python scripts/slugify.py "<Titel>"
python -c "import pathlib,sys; pathlib.Path(sys.argv[1]).rename(sys.argv[2])" wiki/publikationen/<alt>.md wiki/publikationen/<slug>.md
```

Validieren (FAIL → Stub korrigieren, sonst Paper in „Fehlgeschlagen“ der Queue):

```bash
python scripts/normalize_frontmatter.py
python scripts/check_stub_format.py wiki/publikationen/<slug>.md
python scripts/check_stub_numbers.py wiki/publikationen/<slug>.md "publikationen/<original>.pdf"
```

Bei jeder Cluster-Wahl, die laut Entscheidungsbaum ein Grenzfall ist, die gewählte ID **und
die plausibelste Alternative** notieren — kommt in die Review-Queue.

### 3. Graph — Node + vorgeschlagene Kanten (zur Review markiert)

Pro neuem Stub einen Node anlegen (network-maker-Logik):

```bash
python scripts/add_to_graph.py wiki/publikationen/<slug>.md
```

Kanten **vorschlagen**, aber konservativ: nur `confidence: hoch` setzen, wenn es eine
explizite Text-/Literaturreferenz oder `edge_notes` gibt. Alles andere als `mittel`/`niedrig`
und **in die Review-Queue als „zu bestätigen“** — nicht stillschweigend trauen. Danach:

```bash
python scripts/validate_graph.py
```

### 4. Fact-Check pro neuem Stub

Den [fact-checker](../fact-checker/SKILL.md) auf jeden neuen Stub anwenden
(`/fact-check single <slug>`). Ergebnis landet unter `wiki/_fact-check/<slug>.md`. Alle
`⚠`/`✗`-Findings in die Review-Queue übernehmen — **keine** Fixes automatisch anwenden.

### 5. Propagieren, damit der PR-Diff vollständig + baubar ist

```bash
python scripts/build_wiki_index.py
python scripts/build_wiki_meta.py
python scripts/sync_to_site.py
```

### 6. Hygiene

```bash
python scripts/check_repo.py --quiet
```

Idempotente Befunde dürfen mit `--fix` bereinigt werden; alles andere in die Queue.

### 7. Log

Datierten Eintrag an `wiki/log.md` anhängen (Datei anlegen, falls sie fehlt). Pro Lauf:
welche Paper neu, welche übersprungen, Link auf den PR.

### 8. Review-Queue schreiben

`wiki/_review-queue.md` **komplett neu schreiben** (siehe Template unten). Genau ein Abschnitt
pro neuem Paper mit den offenen Entscheidungen. Diese Datei ist die „Frage an die Nutzerin“ und
gleichzeitig der PR-Body.

### 9. Stagen — Branch commit + Draft-PR (kein Push auf main!)

```bash
git add -A
git commit -m "Auto-Update Wiki <YYYY-MM-DD>: <N> neue Publikation(en)"
git push -u origin auto/wiki-update-<YYYY-MM-DD>
gh pr create --draft \
  --base main \
  --title "Auto-Update Wiki <YYYY-MM-DD>: <N> neue Publikation(en)" \
  --body-file wiki/_review-queue.md \
  --reviewer philippasigl
```

- **Draft-PR**, damit nichts versehentlich live geht.
- `--reviewer` setzt die Nutzerin als Reviewerin → GitHub schickt ihr automatisch eine
  Benachrichtigungs-Mail (so „fragt“ der Lauf nach Input; kein Gmail-Setup nötig).
- **Niemals** `git push` auf `main`, **niemals** `gh pr merge`. Mergen ist Handarbeit der
  Nutzerin und löst erst dann den Live-Deploy aus.

## Template: `wiki/_review-queue.md`

```markdown
# Review-Queue — Auto-Update <YYYY-MM-DD>

Automatischer Lauf hat **<N> neue Publikation(en)** entworfen. Bitte je Paper die offenen
Punkte prüfen, ggf. im Stub korrigieren, dann den PR mergen (Merge = live).

Branch: `auto/wiki-update-<YYYY-MM-DD>`

## <slug-1>  ([wiki/publikationen/<slug-1>.md](wiki/publikationen/<slug-1>.md))
- **Cluster:** `<gewählt>` — Grenzfall? Alternative: `<alt>`  ☐ ok
- **Kanten:** `<from> → <to>` (confidence: <mittel>)  ☐ bestätigen ☐ verwerfen
- **Fact-Check:** <n> ⚠ / <m> ✗ — siehe `wiki/_fact-check/<slug-1>.md`  ☐ geprüft
- **ignore: yes?** <Übersetzung/Duplikat? sonst „nein“>  ☐ ok
- **Hub-Folgearbeit:** ggf. `/auto-wiki update-all` für `<betroffenes Thema>`

## Fehlgeschlagen / manuell
- `<datei>.pdf` — <Grund: Konvertierung/Validierung> → manuell via /pdf-ingestion

## Nicht in diesem Lauf genommen (Backlog über --max hinaus)
- `<datei>.pdf`
```

## Checkliste

- [ ] Eigener Branch `auto/wiki-update-<datum>`, von aktuellem `main`
- [ ] `download_fachtexte.py` gelaufen, `downloaded`-Liste als Arbeitsliste
- [ ] Jeder neue Stub: konvertiert, vollständig entworfen, `check_stub_format.py` `[OK]`
- [ ] `check_stub_numbers.py` geprüft (Abweichungen in Queue)
- [ ] Nodes via `add_to_graph.py`, `validate_graph.py` läuft durch
- [ ] Kanten konservativ, alle nicht-`hoch` in der Queue als „zu bestätigen“
- [ ] Fact-Check pro Stub gelaufen, Findings in der Queue (keine Auto-Fixes)
- [ ] `build_wiki_index.py`, `build_wiki_meta.py`, `sync_to_site.py` gelaufen
- [ ] `wiki/log.md` ergänzt
- [ ] `wiki/_review-queue.md` neu geschrieben
- [ ] Draft-PR geöffnet, Nutzerin als Reviewerin, **nicht** auf main gepusht, **nicht** gemergt
