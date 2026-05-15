# app/schemas.py (Fortsetzung von Tag 5)

# Gemeinsame Felder für Buchungen
class BookingBase(BaseModel):
    customer_name: str
    customer_email: str
    
# Zum Erstellen einer Buchung brauchen wir nur den Namen, E-Mail und welche Tisch-ID gebucht werden soll
class BookingCreate(BookingBase):
    table_id: int
    
# Die Antwort der API enthält zusätzlich die ID und die berechneten Kosten
class BookingResponse(BookingBase):
    id: int
    table_id: int
    total_cost: float
    
    model_config =
configDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
# Gemeinsame Felder für Tische
class TableBase(BaseModel):
    table_number: int
    location: str
    price: float
    
# Felder, die wir beim Erstellen mitsenden
  (is_available ist automatisch auf True)
 class TableCreate(TableBase):
    pass

# so geben wir den Tisch über die API zurück (inklusive ID und Status)
class TableResponse(TableBase):
    id: int
    is_available: bool
    
    # Ermöglicht pydantic das lesen von SQLAlchemy-ORM-Objekten
    model_config = ConfigDict(from_attributes=True)