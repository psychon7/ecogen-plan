"""ExternalDataService — Restate Service for external API calls.

Each handler wraps an external API call (EPA, EC3, NOAA, NREL, etc.)
with Restate-managed retry, idempotency, and the 4-level fallback:
Live API → Cache → Static Snapshot → Manual Entry escalation.
"""

from __future__ import annotations

import logging
from typing import Any

import restate
from restate import Service, Context

from shared.enums.types import DataFallbackLevel

logger = logging.getLogger(__name__)

external_data_service = Service("ExternalDataService")


# ---------------------------------------------------------------------------
# Climate & weather data (NOAA)
# ---------------------------------------------------------------------------

@external_data_service.handler()
async def fetch_climate_data(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Fetch climate data from NOAA for project location."""
    latitude = request.get("latitude")
    longitude = request.get("longitude")
    data_type = request.get("data_type", "temperature")

    logger.info("Fetching climate data: lat=%s, lon=%s, type=%s", latitude, longitude, data_type)

    # In production: httpx call to NOAA API with retry
    return {
        "source": "NOAA",
        "data_type": data_type,
        "fallback_level": DataFallbackLevel.LIVE_API,
        "data": {},
        "note": "Stub — implement NOAA Climate Data Online API",
    }


# ---------------------------------------------------------------------------
# Grid emissions (EPA eGRID)
# ---------------------------------------------------------------------------

@external_data_service.handler()
async def fetch_grid_emissions(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Fetch grid emission factors from EPA eGRID."""
    zip_code = request.get("zip_code")
    subregion = request.get("subregion")

    logger.info("Fetching eGRID data: zip=%s, subregion=%s", zip_code, subregion)

    return {
        "source": "EPA_eGRID",
        "fallback_level": DataFallbackLevel.LIVE_API,
        "data": {},
        "note": "Stub — implement EPA eGRID API / static dataset lookup",
    }


# ---------------------------------------------------------------------------
# Embodied carbon (EC3 / OpenEPD)
# ---------------------------------------------------------------------------

@external_data_service.handler()
async def fetch_ec3_materials(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Fetch embodied carbon data from EC3 / OpenEPD."""
    material_name = request.get("material_name")
    category = request.get("category")

    logger.info("Fetching EC3 data: material=%s, category=%s", material_name, category)

    return {
        "source": "EC3",
        "fallback_level": DataFallbackLevel.LIVE_API,
        "data": {},
        "note": "Stub — implement EC3/OpenEPD API",
    }


# ---------------------------------------------------------------------------
# Product certifications (WaterSense, ENERGY STAR, GREENGUARD)
# ---------------------------------------------------------------------------

@external_data_service.handler()
async def fetch_watersense_certification(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Check WaterSense certification for a fixture."""
    manufacturer = request.get("manufacturer")
    model = request.get("model")

    logger.info("Checking WaterSense: manufacturer=%s, model=%s", manufacturer, model)

    return {
        "source": "EPA_WaterSense",
        "fallback_level": DataFallbackLevel.LIVE_API,
        "certified": False,
        "data": {},
        "note": "Stub — implement WaterSense Product Database API",
    }


@external_data_service.handler()
async def fetch_energy_star_data(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Fetch ENERGY STAR product data for appliances."""
    product_type = request.get("product_type")
    manufacturer = request.get("manufacturer")

    logger.info("Fetching ENERGY STAR: type=%s, mfr=%s", product_type, manufacturer)

    return {
        "source": "ENERGY_STAR",
        "fallback_level": DataFallbackLevel.LIVE_API,
        "data": {},
        "note": "Stub — implement ENERGY STAR Product API (data.energystar.gov)",
    }


@external_data_service.handler()
async def fetch_greenguard_certification(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Check GREENGUARD / GREENGUARD Gold certification for a product."""
    product_name = request.get("product_name")
    manufacturer = request.get("manufacturer")

    logger.info("Checking GREENGUARD: product=%s, mfr=%s", product_name, manufacturer)

    return {
        "source": "GREENGUARD",
        "fallback_level": DataFallbackLevel.LIVE_API,
        "certified": False,
        "certification_level": None,
        "data": {},
        "note": "Stub — implement UL GREENGUARD API",
    }


# ---------------------------------------------------------------------------
# Flood zones (FEMA)
# ---------------------------------------------------------------------------

@external_data_service.handler()
async def fetch_flood_zone(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Determine FEMA flood zone for project location."""
    latitude = request.get("latitude")
    longitude = request.get("longitude")

    logger.info("Fetching FEMA flood zone: lat=%s, lon=%s", latitude, longitude)

    return {
        "source": "FEMA",
        "fallback_level": DataFallbackLevel.LIVE_API,
        "data": {},
        "note": "Stub — implement FEMA National Flood Hazard Layer API",
    }


# ---------------------------------------------------------------------------
# Solar / renewable energy (NREL)
# ---------------------------------------------------------------------------

@external_data_service.handler()
async def fetch_solar_data(ctx: Context, request: dict[str, Any]) -> dict[str, Any]:
    """Fetch solar resource data from NREL PVWatts."""
    latitude = request.get("latitude")
    longitude = request.get("longitude")
    system_capacity = request.get("system_capacity", 4)

    logger.info("Fetching NREL solar data: lat=%s, lon=%s", latitude, longitude)

    return {
        "source": "NREL_PVWatts",
        "fallback_level": DataFallbackLevel.LIVE_API,
        "data": {},
        "note": "Stub — implement NREL PVWatts API",
    }
