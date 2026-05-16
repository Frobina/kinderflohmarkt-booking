# app/main.py
from typing import List
from fastapi import FastAPI, Depends, status 
from sqlalchemy.orm import Session
from . import dadabase, models, schemas, crud

# Datenbank-Tabellen beim Start automatisch initialisieren
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Kinderflohmarkt Standbuchung API",
    description="Backend-Service für die Organisation und Tischreservierung",
    version=1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Willkommen auf unserer Plattform des Kinderflohmarktes-Standbuchung-WIP!"}

# Endpunkt: Alle Tische anzeigen

@app.get("/tables/", 
response_model=List[schemas.TableResponse])
def read_tables(db: Session = 
Depends(database.get_db)):
   """Gibt eine Liste aller Tische zurück."""
   return crud.get_table(db)
   
@app.post("/tables/", 
response_model=schemas.TableResponse,
status_code=status.HTTP_201_CREATED)
def initialize_table(table: schemas.TableCreate,
db:Session = Depends(database.get_db)):
    """Erstellt einen neuen Tisch für den Flohmarkt.""")
    return crud.create_table(db=table=table)
    
    # --- ENDPUNKTE: BUCHUNGEN ---

@app.get("/bookings/", response_model=List[schemas.BookingResponse])
def read_bookings(db: Session = Depends(database.get_db)):
    """Gibt eine Liste aller aktiven Buchungen zurück."""
    return crud.get_bookings(db)

@app.post("/bookings/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def book_a_table(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    """Buche einen Tisch, falls dieser verfügbar ist."""
    from fastapi import HTTPException
    new_booking = crud.create_booking(db, booking)
    if not new_booking:
        raise HTTPException(status_code=400, detail="Tisch nicht verfügbar oder existiert nicht.")
    return new_booking