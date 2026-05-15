# app/main.py
from fastapi import FastAPI
from app.database import engine, Base

# Erstellt alle Tabellen in der SQLite-Datenbank, falls sie noch nicht existieren
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kinderflohmarkt standbuchung API")

@app.get("/")
def read_root():
    return {"message": "Willkommen auf unserer Plattform des Kinderflohmarktes-Standbuchung-WIP!"}