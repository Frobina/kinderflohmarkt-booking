# Kinderflohmarkt-Standbuchung (WIP)

Eine Moderne, webbasierte Plattform zur Organisation von Kinderflohmärkten im Fokus auf Tisch- und Standbuchungen

##Projektübersicht
Dieses Projekt ist eine 3-Wöchige Agile-Simulation.
Wir nutzen:
-**Backend:** FastAPI (Python)
-**Datenbank:** SQLite3 mit SQLAlchemy
-**Validierung:** Pydantic

## Sprint-Plan
-**Woche 1:**Fundament & Datenstruktur (setup, Models, Schemas)
-**Woche 2:** CRUD-Logik & Tisch-API
-**Woche 3:** Stornierung, Tests & Dokumentation




Das Hauptthema in Woche 3 ist: Stornierungen (Datenkonsistenz) und Automatisierte API-Tests (Skipte). Wir wollen, dass Nutzer ihre Buchung löschen können und dass das System wieder auf "Verfügbar" setzt. Danach schreiben wir ein Skript, das die gesamte API in Sekundenschnelle auf Fehler prüft.

## Installation (Tag 1)
1. Virtuelle Umgebung erstellen:'python-m venv venv'
2. Aktivieren: 'venv\skipts\activate' (Windows) oder 'source venv/bin/activate' (MAc/Linux)
3. Bibliotheken initialisieren: 'pip install -r requirements.txt'