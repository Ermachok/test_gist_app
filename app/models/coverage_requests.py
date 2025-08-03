from sqlalchemy import Column, Integer, Float, DateTime, JSON
from datetime import datetime

from app.db.database import Base


class CoverageRequest(Base):
    __tablename__ = "coverage_requests"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_m = Column(Float, nullable=False)
    area_km2 = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    geojson = Column(JSON, nullable=True)
