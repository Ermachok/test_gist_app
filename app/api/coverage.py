from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio

from app.schemas.coverage import CoverageRequestIn, CoverageResponse
from app.db.session import get_session
from app.utils.cache import get_cached_coverage, save_coverage_to_cache
from app.api.utils.geo import generate_circle_polygon
from app.api.utils.google_sheets import append_row_to_google_sheet
from app.api.utils.logger import logger

router = APIRouter()


@router.post("/coverage", response_model=CoverageResponse)
async def coverage_endpoint(
    request: CoverageRequestIn,
    session: AsyncSession = Depends(get_session),
):
    logger.info(
        f"Received coverage request: lat={request.latitude}, lon={request.longitude}, radius={request.radius_m}"
    )

    cached = await get_cached_coverage(
        session, request.latitude, request.longitude, request.radius_m
    )
    if cached:
        logger.info("Sending cached data to Google Sheets asynchronously.")
        asyncio.create_task(
            append_row_to_google_sheet(
                [
                    datetime.now(ZoneInfo("Europe/Moscow")).isoformat(),
                    request.latitude,
                    request.longitude,
                    request.radius_m,
                    cached["area_km2"],
                ]
            )
        )

        logger.info("Returning cached result.")
        return CoverageResponse(
            geojson=cached["geojson"],
            area_km2=cached["area_km2"],
            source="cache",
        )

    logger.info("No cache found. Computing coverage polygon...")
    await asyncio.sleep(5)

    geojson_polygon, area_km2 = generate_circle_polygon(
        request.latitude, request.longitude, request.radius_m
    )
    logger.debug(f"Computed area (km²): {area_km2:.4f}")

    await save_coverage_to_cache(
        session,
        request.latitude,
        request.longitude,
        request.radius_m,
        area_km2,
        geojson_polygon,
    )
    logger.info("Saved result to cache.")

    logger.info("Sending data to Google Sheets asynchronously.")
    asyncio.create_task(
        append_row_to_google_sheet(
            [
                datetime.now(ZoneInfo("Europe/Moscow")).isoformat(),
                request.latitude,
                request.longitude,
                request.radius_m,
                area_km2,
            ]
        )
    )

    logger.info("Returning newly computed result.")
    return CoverageResponse(
        geojson=geojson_polygon,
        area_km2=area_km2,
        source="computed",
    )
