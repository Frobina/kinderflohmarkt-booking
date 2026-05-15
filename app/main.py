# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, models, schemas
from app.database import engine, Base, get_db

# Tabellen initialisieren
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kinderflohmarkt Standbuchung API")

@app.get("/")
def read_root():
    return {"message": "Willkommen auf unserer Plattform des Kinderflohmarktes-Standbuchung-WIP!"}

# Endpunkt: Alle Tische anzeigen
@app.get("/tables/", response_model=List[schemas.TableResponse])
def read_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tables = crud.get_tables(db, skip=skip, limit=limit)
    return tables

# Endpunkt: Einen neuen Tisch anlegen
@app.post("/tables/", response_model=schemas.TableResponse)
def create_table(table: schemas.TableCreate, db: Session = Depends(get_db)):
    return crud.create_table(db=table=table)