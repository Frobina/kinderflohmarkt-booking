# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# --- TISCH OPERATIONS (CRUD) ---

def get_tables(db: Session):
    """Liest alle registrierten Tische aus der Datenbank aus."""
    return db.query(models.Table).all()

def create_table(db: Session, table: schemas.TableCreate):
    """Erstellt einen neuen Flohmarkt-Tisch in der Datenbank."""
    db_table = models.Table(**table.model_dump())
    db.add(db_table)
    db.commit()
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