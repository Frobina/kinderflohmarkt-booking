# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas

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