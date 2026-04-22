from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Autobus(Base):
    """Represents a bus (autobús) in the transportation system.
    
    Attributes:
        id: Primary key identifier.
        vehiculo: Vehicle identifier (integer).
        posicion: Geographic Point geometry representing the current location (SRID 4326).
        sentido: Direction of travel (1 or 2).
        linea_id: Foreign key reference to the Linea (bus line).
        linea: Relationship to Linea.
    """

    __tablename__ = "autobus"

    id = Column(Integer, primary_key=True, index=True)
    vehiculo = Column(Integer, nullable=False, index=True)
    posicion = Column(Geometry("POINT", srid=4326), nullable=False)
    sentido = Column(Integer, nullable=False)
    linea_id = Column(Integer, ForeignKey("linea.id"), nullable=False, index=True)

    # Relationship to Linea
    linea = relationship("Linea")

    def __repr__(self) -> str:
        return f"<Autobus(id={self.id}, vehiculo={self.vehiculo}, sentido={self.sentido})>"
