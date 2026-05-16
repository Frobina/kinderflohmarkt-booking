# app/crud.py
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

# --- TISCH OPERATIONS (CRUD) ---

def get_tables(db: Session) -> List[models.Table]:
    """Liest alle registrierten Tische aus der Datenbank aus."""
    return db.query(models.Table).all()

def create_table(db: Session, table: schemas.TableCreate) -> models.Table:
    """Erstellt einen neuen Flohmarkt-Tisch in der Datenbank."""
    db_table = models.Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

# --- BUCHUNG OPERATIONS (CRUD) ---

def get_bookings(db: Session) -> List[models.Booking]:
    """Liest alle bestehenden Buchungen aus der Datenbank aus."""
    return db.query(models.Booking).all()

def create_booking(db: Session, booking: schemas.BookingCreate) -> Optional[models.Booking]:
    """Prüft die Verfügbarkeit eines Tisches und erstellt die Buchung."""
    table = db.query(models.Table).filter(models.Table.id == booking.table_id).first()
    
    # Validierung: Existiert der Tisch und ist er frei?
    if not table or not table.is_available:
        return None
    
    # Kostenübergabe und Buchungserstellung
    db_booking = models.Booking(
        customer_name=booking.customer_name,
        email=booking.email,
        attendees_count=booking.attendees_count,
        table_id=booking.table_id,
        total_cost=table.price
    )
    
    # Zustand des Tisches im gleichen Schritt aktualisieren
    table.is_available = False
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int) -> bool:
    """
    Löscht eine Buchung aus der Datenbank und gibt den verknüpften 
    Tisch automatisch wieder für neue Buchungen frei.
    """
    # 1. Such nach der existierenden Buchung
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    
    if booking:
        # 2. Such den verknüpften Tisch über die table_id der Buchung
        table = db.query(models.Table).filter(models.Table.id == booking.table_id).first()
        if table:
            # 3. Tisch wieder als verfügbar markieren
            table.is_available = True
        
        # 4. Buchung aus der Datenbank löschen
        db.delete(booking)
        db.commit()
        return True  # Löschen war erfolgreich
        
    return False  # Buchung existierte nicht