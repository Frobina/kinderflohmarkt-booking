app/main.py
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
    # Zusätzliche Validierung: Existiert die Tischnummer bereits?
    existing_table = db.query(models.Table).filter(models.Table.table_number == table.table_number).first()
    if existing_table:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ein Tisch mit der Nummer '{table.table_number}' existiert bereits."
        )
    return crud.create_table(db, table)


# --- ENDPUNKTE: BUCHUNGEN ---

@app.get("/bookings/", response_model=List[schemas.BookingResponse], status_code=status.HTTP_200_OK)
def read_bookings(db: Session = Depends(database.get_db)):
    return crud.get_bookings(db)


@app.post("/bookings/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def book_a_table(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    # Validierung: Existiert der Tisch überhaupt in der Datenbank?
    table_exists = db.query(models.Table).filter(models.Table.id == booking.table_id).first()
    if not table_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tisch-ID {booking.table_id} existiert nicht."
        )
        
    new_booking = crud.create_booking(db, booking)
    if not new_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Dieser Tisch ist leider bereits von einem anderen Teilnehmer ausgebucht."
        )
    return new_booking


# --- ENDPUNKTE: STORNIERUNGEN ---

@app.delete("/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def cancel_booking(booking_id: int, db: Session = Depends(database.get_db)) -> dict:
    success = crud.delete_booking(db, booking_id=booking_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stornierung fehlgeschlagen: Buchungs-ID {booking_id} existiert nicht."
        )
        
    return {"message": f"Buchung {booking_id} wurde erfolgreich storniert. Der Tisch steht wieder zur Verfügung."}