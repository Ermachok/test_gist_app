from sqlalchemy.future import select
from app.models.coverage_requests import CoverageRequest
from sqlalchemy.ext.asyncio import AsyncSession
import json
import geojson


async def get_cached_coverage(session: AsyncSession, lat: float, lon: float, radius_m: float):
    result = await session.execute(
        select(CoverageRequest).where(
            CoverageRequest.latitude == lat,
            CoverageRequest.longitude == lon,
            CoverageRequest.radius_m == radius_m,
        )
    )
    obj = result.scalars().first()
    if obj:
        return {
            "geojson": geojson.loads(obj.geojson),
            "area_km2": obj.area_km2,
        }
    return None


async def save_coverage_to_cache(session: AsyncSession, lat: float, lon: float, radius_m: float, area_km2: float, geojson_polygon):
    geojson_str = json.dumps(geojson_polygon)
    obj = CoverageRequest(
        latitude=lat,
        longitude=lon,
        radius_m=radius_m,
        area_km2=area_km2,
        geojson=geojson_str,
    )
    session.add(obj)
    await session.commit()
