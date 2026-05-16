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
        "table_id": 1  # Wir buchen den ersten Tisch (Tisch-A1)
    }
    
    response_pos = requests.post(f"{BASE_URL}/bookings/", json=valide_buchung)
    
    if response_pos.status_code == 201:
        booking_data = response_pos.json()
        print(f"✅ Erfolg: Tisch 1 gebucht! Buchungs-ID: {booking_data['id']}, Gesamtkosten: {booking_data['total_cost']}€")
    else:
        print(f"❌ Fehler bei der validen Buchung: {response_pos.text}")
    print()

    # --- PHASE 3: FEHLERTEST (DOPPELBUCHUNG BLOCKIEREN) ---
    print("--- Phase 3: Fehlertest (Doppelbuchung blockieren) ---")
    doppel_buchung = {
        "customer_name": "Maximilian Mustermann",
        "email": "max@example.com",
        "attendees_count": 1,
        "table_id": 1  # Versucht, exakt denselben Tisch (ID 1) noch mal zu buchen
    }
    
    response_neg = requests.post(f"{BASE_URL}/bookings/", json=doppel_buchung)
    
    # Hier erwarten wir einen 400er Fehler, weil das Backend den Tisch gesperrt hat
    if response_neg.status_code == 400:
        print("✅ Erfolg: Die Doppelbuchung wurde vom Backend wie erwartet blockiert!")
        print(f"   Meldung vom Server: {response_neg.json()['detail']}")
    else:
        print(f"❌ FEHLER: Das Backend hätte diese Buchung blockieren müssen! Status: {response_neg.status_code}")
        print(f"   Antwort: {response_neg.text}")

if __name__ == "__main__":
    try:
        run_api_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ FEHLER: Das Backend läuft scheinbar nicht!")
        print("Bitte starte zuerst 'uvicorn app.main:app --reload' in einem separaten Terminal.")