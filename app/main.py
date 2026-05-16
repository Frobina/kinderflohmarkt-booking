# app/main.py
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database, models, schemas, crud

# Datenbank-Tabellen beim Start initialisieren
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Kinderflohmarkt Standbuchung API",
    description="Backend-Service für die Organisation und Tischreservierung",
    version="1.0.0"
)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root() -> dict:
    return {"message": "Willkommen beim Kinderflohmarkt-Standbuchungs-API-Service!"}

# --- ENDPUNKTE: TISCHE ---

@app.get("/tables/", response_model=List[schemas.TableResponse], status_code=status.HTTP_200_OK)
def read_tables(db: Session = Depends(database.get_db)):
    return crud.get_tables(db)

@app.post("/tables/", response_model=schemas.TableResponse, status_code=status.HTTP_201_CREATED)
def initialize_table(table: schemas.TableCreate, db: Session = Depends(database.get_db)):
    return crud.create_table(db, table)

# --- ENDPUNKTE: BUCHUNGEN ---

@app.get("/bookings/", response_model=List[schemas.BookingResponse], status_code=status.HTTP_200_OK)
def read_bookings(db: Session = Depends(database.get_db)):
    return crud.get_bookings(db)

@app.post("/bookings/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def book_a_table(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    new_booking = crud.create_booking(db, booking)
    if not new_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Tisch nicht verfügbar oder existiert nicht."
        )
    return new_booking

# --- ENDPUNKTE: STORNIERUNGEN ---

@app.delete("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def cancel_booking(booking_id: int, db: Session = Depends(database.get_db)) -> dict:
    """
    Storniert eine bestehende Buchung anhand ihrer ID und 
    gibt den Tisch automatisch wieder frei.
    """
    success = crud.delete_booking(db, booking_id=booking_id)
    
    # Wenn die Buchung nicht gefunden wurde, Fehlermeldung zurückgeben
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Buchung mit der ID {booking_id} wurde nicht gefunden."
        )
        
    return {"message": f"Buchung {booking_id} wurde erfolgreich storniert. Der Tisch ist wieder frei."}