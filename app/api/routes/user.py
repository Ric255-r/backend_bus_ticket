from typing import Optional
from math import atan2, cos, radians, sin, sqrt
from time import monotonic
import uuid
from fastapi import (
  APIRouter,
  File,
  Form,
  Query,
  Request,
  HTTPException,
  Security,
  UploadFile,
)
from fastapi.responses import JSONResponse, FileResponse
from app.core.database import conn
from fastapi_jwt import (
  JwtAccessBearerCookie,
  JwtAuthorizationCredentials,
  JwtRefreshBearer,
)
from app.core.security import access_security, refresh_security
import pandas as pd
import httpx
import os

router = APIRouter()

IMAGEDIR = "images/profile"
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
OVERPASS_USER_AGENT = os.getenv(
  "OVERPASS_USER_AGENT", "BusHub/1.0 (portfolio application)"
)
POI_CACHE_TTL_SECONDS = 600
poi_cache = {}


@router.get("/fotoprofile/{filename}")
def fnProfile(filename: str):
  img_path = os.path.join(IMAGEDIR, filename)
  return FileResponse(img_path, media_type="image/png")


@router.get("/user")
def fnUser(user: JwtAuthorizationCredentials = Security(access_security)):
  cursor = conn.cursor()
  query = "SELECT * FROM users WHERE email = %s"
  cursor.execute(query, (user["email"],))

  column_name = []
  for kol in cursor.description:
    column_name.append(kol[0])

  items = cursor.fetchall()

  # Buat bentuk df
  df = pd.DataFrame(items, columns=column_name)

  # konversi field tgllahir ke str
  df = df.applymap(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)

  # Jadikan json
  subject = df.to_dict("records")[0]  # pecahkan arraynya

  # Pop password
  subject.pop("passwd", None)

  return subject


@router.post("/register")
async def fnRegis(request: Request):
  cursor = conn.cursor()

  try:
    data = await request.json()
    username = data["username"]
    email = data["email"]
    passwd = data["passwd"]

    # Cek Email ad atau nd
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    itemEmail = cursor.fetchall()

    if len(itemEmail) > 0:
      return JSONResponse(
        content={"Error": "Email Sudah Terdaftar"}, status_code=409
      )  # code duplicate
    else:
      insQuery = "INSERT INTO users(username, email, passwd) VALUES(%s, %s, %s)"
      cursor.execute(insQuery, (username, email, passwd))
      conn.commit()

      return JSONResponse(content={"Success": "Email Terdaftar"}, status_code=200)

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()


@router.post("/login")
async def fnLogin(request: Request):
  cursor = conn.cursor()
  try:
    # dia nerima data dalam bentuk raw/json.
    data = await request.json()
    passwd = data["passwd"]

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (data["email"],))

    # kalau cmn fetchall() itu dia hny ambil values. jd ak mw ambil nama kolomnya jg
    column_names = []
    for kol in cursor.description:
      column_names.append(kol[0])

    items = cursor.fetchall()

    if not items:
      raise HTTPException(status_code=404, detail="User Not Found")

    stored_pass = items[0][
      3
    ]  # ambil index passwd. dia dilapis tuple lalu ada list. jadi 2D

    if passwd != stored_pass:
      raise HTTPException(status_code=401, detail="Password Salah")

    # Buat Dataframe. jadi ada isi item dan nama field.
    df = pd.DataFrame(items, columns=column_names)

    # konversi tgl_lahir ke string.
    df = df.applymap(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)

    # buat return bentuk json, tapi ad bbrp kolom yg di ilangin
    subject = df.to_dict("records")[0]

    # Hilangkan record passwd
    subject.pop("passwd", None)
    subject.pop("created_at", None)

    # Buat token
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return {
      "usernya": subject,
      "access_token": access_token,
      "refresh_token": refresh_token,
    }
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()


@router.put("/updateProfile")
async def updateProfile(
  fotoProfile: Optional[UploadFile] = File(None),
  username: str = Form(...),
  email: str = Form(...),
  nohp: str = Form(...),
  tanggal_lahir: str = Form(...),
  jk: bool = Form(...),
  user: JwtAuthorizationCredentials = Security(access_security),
):
  print(fotoProfile)
  print(username)
  print(email)
  print(nohp)
  print(jk)

  # return

  try:
    cursor = conn.cursor()

    if fotoProfile is None:
      q1 = """
        UPDATE users SET username = %s, no_hp = %s, jk = %s, tanggal_lahir = %s
        WHERE id = %s
      """

      cursor.execute(q1, (username, nohp, jk, tanggal_lahir, user["id"]))
      conn.commit()
    else:
      filename = f"{uuid.uuid4()}.png"
      file_location = os.path.join(IMAGEDIR, filename)

      # saveFile
      content = await fotoProfile.read()
      with open(file_location, "wb") as f:
        f.write(content)

      q1 = """
        UPDATE users SET username = %s, profile_picture = %s, no_hp = %s, jk = %s, tanggal_lahir = %s
        WHERE id = %s
      """

      cursor.execute(q1, (username, filename, nohp, jk, tanggal_lahir, user["id"]))
      conn.commit()

    return JSONResponse(content={"Pesan": "Sukses Update"}, status_code=200)

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)

  finally:
    cursor.close()


@router.put("/changePass")
async def fnChangePass(
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security),
):
  try:
    cursor = conn.cursor()
    data = await request.json()

    oldPasswd = data["oldPass"]
    newPasswd = data["newPass"]

    q1 = "SELECT * FROM users WHERE email = %s AND passwd = %s"
    cursor.execute(q1, (user["email"], oldPasswd))

    items = cursor.fetchall()

    if not items:
      return JSONResponse(
        content={"Error": "Password Lama Tidak Cocok"}, status_code=401
      )

    else:
      q2 = "UPDATE users SET passwd = %s WHERE email = %s"
      cursor.execute(q2, (newPasswd, user["email"]))
      conn.commit()

      return JSONResponse(
        content={"Success": "Password Sudah Diganti"}, status_code=200
      )

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)

  finally:
    cursor.close()


def _distance_km(latitude1, longitude1, latitude2, longitude2):
  earth_radius_km = 6371.0
  latitude_delta = radians(latitude2 - latitude1)
  longitude_delta = radians(longitude2 - longitude1)
  value = (
    sin(latitude_delta / 2) ** 2
    + cos(radians(latitude1)) * cos(radians(latitude2)) * sin(longitude_delta / 2) ** 2
  )
  return earth_radius_km * 2 * atan2(sqrt(value), sqrt(1 - value))


def _normalize_poi(element, user_latitude, user_longitude):
  center = element.get("center", {})
  latitude = element.get("lat", center.get("lat"))
  longitude = element.get("lon", center.get("lon"))
  if latitude is None or longitude is None:
    return None

  tags = element.get("tags", {})
  name = (
    tags.get("name")
    or tags.get("ref")
    or tags.get("amenity")
    or tags.get("tourism")
    or "Tempat tanpa nama"
  )

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
    "amenity": tags.get("amenity"),
    "tourism": tags.get("tourism"),
    "leisure": tags.get("leisure"),
    "opening_hours": tags.get("opening_hours"),
    "phone": tags.get("phone"),
    "website": tags.get("website"),
  }


@router.get("/poi-terdekat")
async def nearby_pois(
  latitude: float = Query(..., ge=-90, le=90),
  longitude: float = Query(..., ge=-180, le=180),
  category: str = Query("kuliner"),
  radius: int = Query(3000, ge=500, le=10000),
  limit: int = Query(20, ge=1, le=50),
):
  category = category.lower()
  # Map categories to OSM filters
  category_filters = {
    "kuliner": [
      'nwr["amenity"="restaurant"]',
      'nwr["amenity"="cafe"]',
      'nwr["amenity"="fast_food"]',
      'nwr["amenity"="food_court"]',
    ],
    "ibadah": [
      'nwr["amenity"="place_of_worship"]',
    ],
    "kesehatan": [
      'nwr["amenity"="hospital"]',
      'nwr["amenity"="pharmacy"]',
      'nwr["amenity"="clinic"]',
      'nwr["amenity"="doctors"]',
    ],
    "penginapan": [
      'nwr["tourism"="hotel"]',
      'nwr["tourism"="motel"]',
      'nwr["tourism"="guest_house"]',
      'nwr["tourism"="hostel"]',
    ],
    "atm": [
      'nwr["amenity"="atm"]',
      'nwr["amenity"="bank"]',
    ],
    "wisata": [
      'nwr["tourism"="attraction"]',
      'nwr["tourism"="viewpoint"]',
      'nwr["tourism"="museum"]',
      'nwr["leisure"="park"]',
    ],
  }

  filters = category_filters.get(category, category_filters["kuliner"])

  # Build query
  statements = "\n".join(
    [f"{f}(around:{radius},{latitude},{longitude});" for f in filters]
  )

  overpass_query = f"""
    [out:json][timeout:20];
    (
      {statements}
    );
    out center tags;
  """

  # Cache key
  cache_key = (round(latitude, 3), round(longitude, 3), category, radius)
  cached = poi_cache.get(cache_key)
  if cached and monotonic() - cached["created_at"] < POI_CACHE_TTL_SECONDS:
    return {
      "source": "OpenStreetMap via Overpass API",
      "cached": True,
      "category": category,
      "count": min(limit, len(cached["items"])),
      "items": cached["items"][:limit],
    }

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
      detail="Data POI dari OpenStreetMap sedang tidak tersedia.",
    ) from error

  unique_items = {}
  for element in payload.get("elements", []):
    item = _normalize_poi(element, latitude, longitude)
    if item is not None:
      unique_items[item["osm_id"]] = item

  items = sorted(unique_items.values(), key=lambda item: item["distance_km"])
  poi_cache[cache_key] = {"created_at": monotonic(), "items": items}

  return {
    "source": "OpenStreetMap via Overpass API",
    "cached": False,
    "category": category,
    "count": min(limit, len(items)),
    "items": items[:limit],
  }
