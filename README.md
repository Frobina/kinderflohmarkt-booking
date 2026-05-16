# Kinderflohmarkt-Plattform - Backend

Eine moderne Web-Applikation zur Organisation von Kinderflohmärkten mit Fokus auf Tisch- und Standbuchungen. Dieses Projekt wurde als stabiler, funktionsfähiger Prototyp (MVP) im Rahmen eines 3-wöchigen agilen Sprints entwickelt.

## 🚀 Technologie-Stack
- **Framework:** FastAPI (Python)
- **Datenbank:** SQLite via SQLAlchemy (ORM)
- **Validierung:** Pydantic v2
- **Testing:** Python Requests-Bibliothek
- **Server:** Uvicorn

## 📅 Sprint 1: Core Buchungs-Engine
Simulation eines 3-wöchigen agilen Sprints mit der Disziplin von täglichen Commits (Daily Commits).

### 🛠️ Fortschritts-Fahrplan

#### Woche 1: Fundament & Datenstruktur
- [x] Tag 1: Projekt-Setup & Git-Initialisierung
- [x] Tag 2: Datenbank-Verbindung (`app/database.py`)
- [x] Tag 3: Das Tisch-Modell (`app/models.py`)
- [x] Tag 4: Das Buchungs-Modell mit Beziehungen (`app/models.py`)
- [x] Tag 5: Pydantic-Schemas für Tisch-Validierung (`app/schemas.py`)
- [x] Tag 6: Pydantic-Schemas für Buchungs-Validierung (`app/schemas.py`)
- [x] Tag 7: Minimale Hauptanwendung initialisieren (`app/main.py`)

#### Woche 2: CRUD-Logik & Tisch-API
- [x] Tag 8: CRUD-Funktionen für Tische schreiben (`app/crud.py`)
- [x] Tag 9: API-Endpunkte für Tische bereitstellen (`app/main.py`)
- [x] Tag 10: Manuelle API-Tests via FastAPI Swagger-UI (`/docs`)
- [x] Tag 11: Basis-CRUD-Abfrage für Buchungen erstellen (`app/crud.py`)
- [x] Tag 12: Kern-Logik für Verfügbarkeitsprüfung & Kostenberechnung (`app/crud.py`)
- [x] Tag 13: API-Endpunkte für Buchungen bereitstellen (`app/main.py`)
- [x] Tag 14: Mid-Sprint Review & Code-Refactoring (Typisierung geglättet)

#### Woche 3: Stornierung & Automatisierte API-Tests
- [x] Tag 15: CRUD-Logik für Buchungsstornierung (Tisch freigeben)
- [x] Tag 16: API-Endpunkt für DELETE-Anfragen einbauen
- [x] Tag 17: Test-Skript Setup für automatisierte Anfragen
- [x] Tag 18: Buchungssimulation & Fehlertests im Skript einbauen
- [x] Tag 19: Stornierungssimulation im Testskript automatisieren
- [x] Tag 20: Fehlerbehandlung & HTTP-Statuscodes vereinheitlichen
- [x] Tag 21: Sprint-Review & finale README-Dokumentation

---

## 💻 Lokaler Start (Entwicklungsmodus)

1. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt