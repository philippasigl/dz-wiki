@echo off
REM ============================================================================
REM  DZ Wiki - lokaler Auto-Update-Starter
REM ----------------------------------------------------------------------------
REM  Oeffnet eine interaktive Claude-Code-Session im Repo, vorbelegt mit dem
REM  /wiki-auto-update-Skill. Die Session fragt bei jedem Schritt (Scrape, Push,
REM  PR) nach Bestaetigung -- "scheduled, but I confirm".
REM
REM  WARUM LOKAL: Der Scraper (download_fachtexte.py) bekommt aus der Anthropic-
REM  Cloud 403 von dezernatzukunft.org (IP-blockiert). Vom lokalen Rechner aus
REM  ist die Website erreichbar, deshalb laeuft der Update-Job hier statt als
REM  Remote-Routine.
REM
REM  Wird i. d. R. von der Windows-Aufgabe "DZ Wiki Auto-Update" alle 2 Wochen
REM  gestartet, kann aber auch per Doppelklick manuell ausgefuehrt werden.
REM ============================================================================

set "REPO=%~dp0.."
wt.exe -d "%REPO%" --title "DZ Wiki Auto-Update" cmd /k claude "/wiki-auto-update"
