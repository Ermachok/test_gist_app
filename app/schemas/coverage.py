from pydantic import BaseModel, confloat
from typing import Literal


class CoverageRequestIn(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)
    radius_m: confloat(gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "latitude": 55.751244,
                "longitude": 37.618423,
                "radius_m": 500,
            }
        }


class CoverageResponse(BaseModel):
    geojson: dict
    area_km2: float
    source: Literal["cache", "computed"]
