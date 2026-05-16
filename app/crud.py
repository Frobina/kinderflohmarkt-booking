# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# --- TISCH OPERATIONS (CRUD) ---

def get_tables(db: Session):
    """Liest alle registrierten Tische aus der Datenbank aus.
    Wird später vom GET-Endpunkt aufgerufen."""
    return db.query(models.Table).all()

def create_table(db: Session, table: schemas.TableCreate):
    """Erstellt einen neuen Flohmarkt-Tisch in der Datenbank. Nimmt die Validierten Daten aus dem Pydantic-Schema und wandelt sie in ein SQLAlchemy-Modell um."""
    # .model_dump() wandelt das Pydantic-Objekt in ein Python-Dictionary um
    db_table = 
    models.Table(**table.model_dump())
    
    # In die Datenbank einfügen und speichern
    db.add(db_table)
    db.commit()
    
    # Das Objekt aktualisieren, damit es von der DB generierte ID enthält
    db.refresh(db_table)
    return db_table

# 1. Alle Tische aus der Datenbank abrufen
def get_tables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Table).offset(skip).limit(limit).all()

# 2. Einen neuen Tisch in der Datenbank anlegen
def create_table(db: Session, table:
schemas.TableCreate):
    db_table = models.Table(
        table_number=table.table_number,
        locaition=table.location,
        price=table.price
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table) # Lädt die gernerierte ID aus der DB nach 
    return db_table

# --- BUCHUNG OPERATIONS (CRUD) ---


def get_bookings(db: Session):
    """Liest alle bestehenden Buchungen aus der Datenbank aus."""
    return db.query(models.Booking).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    """Prüft die Verfügbarkeit eines Tisches und erstellt die Buchung."""
    # 1. Prüfen, ob der Tisch existiert und aktuell noch frei ist
    table = db.query(models.Table).filter(models.Table.id == booking.table_id).first()
    if not table or not table.is_available:
        return None  # Signalisiert der API, dass die Buchung fehgeschlagen ist
    
    # 2. Kosten automatisch aus dem Tischpreis übernehmen
    calculated_cost = table.price

    # 3. Buchungsobjekt erstellen
    db_booking = models.Booking(
        customer_name=booking.customer_name,
        email=booking.email,
        attendees_count=booking.attendees_count,
        table_id=booking.table_id,
        total_cost=calculated_cost
    )
    
    # 4. Tisch als reserviert (nicht mehr verfügbar) markieren
    table.is_available = False
    
    # 5. In der Datenbank speichern
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking