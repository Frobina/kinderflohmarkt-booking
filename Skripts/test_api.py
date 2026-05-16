import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def run_api_tests():
    print("=========================================")
    print("🚀 STARTE AUTOMATISIERTE API-TESTSIMULATION")
    print("=========================================\n")

    # --- PHASE 1: TEST-TISCHE ANLEGEN ---
    print("--- Phase 1: Erstelle Test-Tische ---")
    test_tables = [
        {"table_number": "Tisch-A1", "location_info": "Halle Nord, Reihe 1", "price": 15.0},
        {"table_number": "Tisch-A2", "location_info": "Halle Nord, Reihe 1", "price": 15.0},
        {"table_number": "Premium-01", "location_info": "Foyer Haupteingang", "price": 25.0}
    ]
    
    for table_data in test_tables:
        requests.post(f"{BASE_URL}/tables/", json=table_data)
    print("✅ Test-Tische erfolgreich initialisiert.\n")

    # --- PHASE 2: ERSTE ERFOLGREICHE BUCHUNG ---
    print("--- Phase 2: Valide Buchung absetzen ---")
    valide_buchung = {
        "customer_name": "Anna König",
        "email": "anna.koenig@example.com",
        "attendees_count": 2,
        "table_id": 1
    }
    
    response_pos = requests.post(f"{BASE_URL}/bookings/", json=valide_buchung)
    booking_id = None
    
    if response_pos.status_code == 201:
        booking_data = response_pos.json()
        booking_id = booking_data['id']
        print(f"✅ Erfolg: Tisch 1 gebucht! Buchungs-ID: {booking_id}, Gesamtkosten: {booking_data['total_cost']}€")
    else:
        print(f"❌ Fehler bei der validen Buchung: {response_pos.text}")
    print()

    # --- PHASE 3: FEHLERTEST (DOPPELBUCHUNG BLOCKIEREN) ---
    print("--- Phase 3: Fehlertest (Doppelbuchung blockieren) ---")
    doppel_buchung = {
        "customer_name": "Maximilian Mustermann",
        "email": "max@example.com",
        "attendees_count": 1,
        "table_id": 1
    }
    
    response_neg = requests.post(f"{BASE_URL}/bookings/", json=doppel_buchung)
    if response_neg.status_code == 400:
        print("✅ Erfolg: Die Doppelbuchung wurde vom Backend wie erwartet blockiert!")
    else:
        print(f"❌ FEHLER: Das Backend hätte diese Buchung blockieren müssen! Status: {response_neg.status_code}")
    print()

    # --- PHASE 4: STORNIERUNG & TISCH-FREIGABE-PRÜFUNG ---
    print("--- Phase 4: Stornierung & Tisch-Freigabe-Prüfung ---")
    if not booking_id:
        print("❌ Abbruch von Phase 4: Keine gültige Buchungs-ID aus Phase 2 vorhanden.")
        return

    # 1. DELETE-Anfrage senden
    del_response = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
    if del_response.status_code == 200:
        print(f"✅ Erfolg: Buchung {booking_id} erfolgreich storniert.")
    else:
        print(f"❌ Fehler bei Stornierung: {del_response.text}")

    # 2. Prüfen, ob der Tisch wirklich wieder frei ist
    tables_response = requests.get(f"{BASE_URL}/tables/")
    if tables_response.status_code == 200:
        tische = tables_response.json()
        # Wir suchen nach dem Tisch mit ID 1 (Tisch-A1)
        tisch_1 = next((t for t in tische if t["id"] == 1), None)
        
        if tisch_1 and tisch_1["is_available"] is True:
            print("✅ Exzellent! Backend-Datenkonsistenz geprüft: Tisch-A1 ist wieder VERFÜGBAR.")
        else:
            print("❌ FEHLER: Der Tisch ist nach der Stornierung immer noch blockiert!")
    else:
        print(f"❌ Fehler beim Abrufen der Tische: {tables_response.text}")

if __name__ == "__main__":
    try:
        run_api_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ FEHLER: Das Backend läuft scheinbar nicht!")
        print("Bitte starte zuerst 'uvicorn app.main:app --reload' in einem separaten Terminal.")