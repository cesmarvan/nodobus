from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from core.database import Base

class Incidencia(Base):
    """Represents an incident in the transit system.
    
    This model allows each stop to be served by multiple lines, and each line
    to serve multiple stops.
    
    Attributes:
        id: Primary key identifier.
        parada_id: Foreign key referencing Parada.
        linea_id: Foreign key referencing Linea.
        parada: Relationship to Parada.
        linea: Relationship to Linea.
    """
        
    __tablename__ = "incidencia"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    parada_id = Column(Integer, ForeignKey("parada.id"), nullable=True, index=True)
    linea_id = Column(Integer, ForeignKey("linea.id"), nullable=False, index=True)

    # Relationships
    parada = relationship("Parada")
    linea = relationship("Linea")

    def __repr__(self) -> str:
        return f"<Incidencia(id={self.id}, parada_id={self.parada_id}, linea_id={self.linea_id})>"