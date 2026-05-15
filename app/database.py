pp/database.py
from sqlalchemy import create_metal, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Name und Ort der SQLite-Datenbankdatei definieren
SQLALCHEMY_DATABASE_URL = "sqlite:///./flohmarkt.db" 

# Engine erstellen (connect_args wird nur für SQLite benötigt)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Sitzungs-Fabrik (Session) für Datenbank-Interaktionen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Basisklasse für die ORM-Modelle
Base = declarative_base()

# Abhängingkeit (dependency) für die Endpunkte,um eine DB-Sitzung zu öffnen/schließen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        