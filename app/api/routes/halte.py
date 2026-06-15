from math import atan2, cos, radians, sin, sqrt
from time import monotonic

from fastapi import APIRouter, HTTPException, Query

import httpx
import os

router = APIRouter()

OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
OVERPASS_USER_AGENT = os.getenv(
  "OVERPASS_USER_AGENT", "BusHub/1.0 (portfolio application)"
)
HALTE_CACHE_TTL_SECONDS = 600
halte_cache = {}


def _distance_km(latitude1, longitude1, latitude2, longitude2):
  earth_radius_km = 6371.0
  latitude_delta = radians(latitude2 - latitude1)
  longitude_delta = radians(longitude2 - longitude1)
  value = (
    sin(latitude_delta / 2) ** 2
    + cos(radians(latitude1)) * cos(radians(latitude2)) * sin(longitude_delta / 2) ** 2
  )
  return earth_radius_km * 2 * atan2(sqrt(value), sqrt(1 - value))


def _normalize_halte(element, user_latitude, user_longitude):
  center = element.get("center", {})
  latitude = element.get("lat", center.get("lat"))
  longitude = element.get("lon", center.get("lon"))
  if latitude is None or longitude is None:
    return None

  tags = element.get("tags", {})
  name = tags.get("name") or tags.get("ref") or "Halte tanpa nama"

  return {
    "osm_id": f"{element.get('type', 'node')}/{element.get('id')}",
    "name": name,
    "latitude": float(latitude),
    "longitude": float(longitude),
    "distance_km": round(
      _distance_km(
        user_latitude,
        user_longitude,
        float(latitude),
        float(longitude),
      ),
      3,
    ),
    "operator": tags.get("operator"),
    "network": tags.get("network"),
    "ref": tags.get("ref"),
    "shelter": tags.get("shelter"),
    "wheelchair": tags.get("wheelchair"),
  }


@router.get("/halte-terdekat")
async def nearby_bus_stops(
  latitude: float = Query(..., ge=-90, le=90),
  longitude: float = Query(..., ge=-180, le=180),
  radius: int = Query(10000, ge=1000, le=20000),
  limit: int = Query(20, ge=1, le=50),
):
  # Pembulatan koordinat membuat pengguna di area yang sama memakai cache yang sama.
  cache_key = (round(latitude, 3), round(longitude, 3), radius)
  cached = halte_cache.get(cache_key)
  if cached and monotonic() - cached["created_at"] < HALTE_CACHE_TTL_SECONDS:
    return {
      "source": "OpenStreetMap via Overpass API",
      "cached": True,
      "count": min(limit, len(cached["items"])),
      "items": cached["items"][:limit],
    }

  overpass_query = f"""
    [out:json][timeout:20];
    (
      node["highway"="bus_stop"](around:{radius},{latitude},{longitude});
      nwr["public_transport"="platform"]["bus"="yes"](around:{radius},{latitude},{longitude});
    );
    out center tags;
  """

  try:
    timeout = httpx.Timeout(25.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
      response = await client.post(
        OVERPASS_URL,
        data={"data": overpass_query},
        headers={"User-Agent": OVERPASS_USER_AGENT},
      )
      response.raise_for_status()
      payload = response.json()
  except (httpx.HTTPError, ValueError) as error:
    raise HTTPException(
      status_code=502,
      detail="Data halte dari OpenStreetMap sedang tidak tersedia.",
    ) from error

  unique_items = {}
  for element in payload.get("elements", []):
    item = _normalize_halte(element, latitude, longitude)
    if item is not None:
      unique_items[item["osm_id"]] = item

  items = sorted(unique_items.values(), key=lambda item: item["distance_km"])
  halte_cache[cache_key] = {"created_at": monotonic(), "items": items}

  return {
    "source": "OpenStreetMap via Overpass API",
    "cached": False,
    "count": min(limit, len(items)),
    "items": items[:limit],
  }
