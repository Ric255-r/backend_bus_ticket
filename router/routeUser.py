from fastapi import APIRouter, Request, HTTPException, Security
from fastapi.responses import JSONResponse
from koneksi import conn
from fastapi_jwt import (
  JwtAccessBearerCookie,
  JwtAuthorizationCredentials,
  JwtRefreshBearer
)
from jwt_auth import access_security, refresh_security
import pandas as pd

app = APIRouter()

@app.get('/user')
def fnUser(
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  cursor = conn.cursor()
  query = "SELECT * FROM users WHERE email = %s"
  cursor.execute(query, (user['email'], ))

  column_name = []
  for kol in cursor.description:
    column_name.append(kol[0])
  
  items = cursor.fetchall()

  #Buat bentuk df
  df = pd.DataFrame(items, columns=column_name)

  #konversi field tgllahir ke str
  df = df.applymap(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)

  # Jadikan json
  subject = df.to_dict('records')[0] # pecahkan arraynya

  # Pop password
  subject.pop('passwd', None)

  return subject

@app.post('/login')
async def fnLogin(
  request: Request
):
  cursor = conn.cursor()
  try:
    #dia nerima data dalam bentuk raw/json.
    data = await request.json()
    passwd = data['passwd']

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (data['email'], ))

    # kalau cmn fetchall() itu dia hny ambil values. jd ak mw ambil nama kolomnya jg
    column_names = []
    for kol in cursor.description:
      column_names.append(kol[0])

    items = cursor.fetchall()

    if not items:
      raise HTTPException(status_code=404, detail="User Not Found")
    
    stored_pass = items[0][3] #ambil index passwd. dia dilapis tuple lalu ada list. jadi 2D
    
    if passwd != stored_pass:
      raise HTTPException(status_code=401, detail="Password Salah")
    
    # Buat Dataframe. jadi ada isi item dan nama field.
    df = pd.DataFrame(items, columns=column_names)

    #konversi tgl_lahir ke string.
    df = df.applymap(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)

    # buat return bentuk json, tapi ad bbrp kolom yg di ilangin
    subject = df.to_dict('records')[0]

    #Hilangkan record passwd
    subject.pop('passwd', None)

    #Buat token
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return {
      "usernya": subject,
      "access_token": access_token,
      "refresh_token": refresh_token
    }
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()