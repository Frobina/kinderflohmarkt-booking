# app/models.py
from sqlalchemy import Column, integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Table(Base):
    __tablename__ = "tables"
    
    id = Column(Integer, primary key=True, index=True)
table_number = Column(Integer, unique=True, index=True, nullable=False) 
location = Column(String, nullable=False) 
Price = Column(Float, nullalable=False)
is_available = Column(Boolean, default=True)
   
   # Beziehungen zu den Buchungen (Ein Tisch kann theoretisch mehrere Buchungen haben)
   bookings = relationship ("Booking", back_populates="table")
    
class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
      totsl_cost = Column(Float, nullable=False)
      
      # Fremdschlüssel-Verknüfung zum Tisch (jede Buchung gehört zu einem Tisch)
     table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
     
      # Beziehungsdefinition zurück zum Tisch-Objekt
    table = relationship("Table", back_populates="bookings")