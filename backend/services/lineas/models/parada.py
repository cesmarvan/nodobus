"""Models for the Lineas service."""

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Parada(Base):
    """Represents a stop (parada) in the transportation system.
    
    Attributes:
        id: Primary key identifier.
        nodo: Integer identifer for the node.
        nombre: Name of the stop.
        localizacion: Geographic point location of the stop.
        parada_lineas: Relationship to ParadaLinea for many-to-many mapping with Linea.
    """

    __tablename__ = "parada"

    id = Column(Integer, primary_key=True, index=True)
    nodo = Column(Integer, index=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    localizacion = Column(Geometry("POINT", srid=4326), nullable=False)

    # Relationship to ParadaLinea for many-to-many mapping
    parada_lineas = relationship(
        "ParadaLinea", back_populates="parada", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Parada(id={self.id}, nodo={self.nodo}, nombre='{self.nombre}')>"





