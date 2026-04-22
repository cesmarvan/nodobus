from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base

class Linea(Base):
    """Represents a bus line (línea) in the transportation system.
    
    Attributes:
        id: Primary key identifier.
        color: Hex color code for the line (stored as string).
        destino: Destination of the line.
        labelLinea: Label identifier for the line.
        linea: Integer identifier for the line.
        nombreLinea: Name of the line.
        recorrido: Geographic LineString geometry representing the route.
        parada_lineas: Relationship to ParadaLinea for many-to-many mapping with Parada.
    """

    __tablename__ = "linea"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String(7), nullable=False)  # Hex color code (e.g., '#FF5733')
    destino = Column(String(255), nullable=False)
    labelLinea = Column(String(50), nullable=False)
    linea = Column(Integer, nullable=False, index=True)
    nombreLinea = Column(String(255), nullable=False)
    recorrido = Column(Geometry("LINESTRING", srid=4326), nullable=False)

    # Relationship to ParadaLinea for many-to-many mapping
    parada_lineas = relationship(
        "ParadaLinea", back_populates="linea", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Linea(id={self.id}, linea={self.linea}, nombreLinea='{self.nombreLinea}')>"
