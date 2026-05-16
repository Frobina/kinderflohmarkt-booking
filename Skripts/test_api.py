import requests
import json

# Die URL, unter der dein FastAPI-Server lokal läuft
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
        response = requests.post(f"{BASE_URL}/tables/", json=table_data)
        
        if response.status_code == 201:
            created_table = response.json()
            print(f"✅ Erfolg: {created_table['table_number']} angelegt (ID: {created_table['id']})")
        else:
            print(f"❌ Fehler beim Erstellen von {table_data['table_number']}: {response.text}")

if __name__ == "__main__":
    try:
        run_api_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ FEHLER: Das Backend läuft scheinbar nicht!")
        print("Bitte starte zuerst 'uvicorn app.main:app --reload' in einem separaten Terminal.")