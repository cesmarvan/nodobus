from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base

class ParadaLinea(Base):
    """Represents the many-to-many relationship between Parada and Linea.
    
    This model allows each stop to be served by multiple lines, and each line
    to serve multiple stops.
    
    Attributes:
        id: Primary key identifier.
        parada_id: Foreign key referencing Parada.
        linea_id: Foreign key referencing Linea.
        parada: Relationship to Parada.
        linea: Relationship to Linea.
    """

    __tablename__ = "parada_linea"

    id = Column(Integer, primary_key=True, index=True)
    parada_id = Column(Integer, ForeignKey("parada.id", ondelete="CASCADE"), nullable=False, index=True)
    linea_id = Column(Integer, ForeignKey("linea.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    parada = relationship("Parada", back_populates="parada_lineas")
    linea = relationship("Linea", back_populates="parada_lineas")

    def __repr__(self) -> str:
        return f"<ParadaLinea(parada_id={self.parada_id}, linea_id={self.linea_id})>"