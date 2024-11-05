from typing import Optional
import uuid
from fastapi import APIRouter, File, Form, Request, HTTPException, Security, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from koneksi import conn
from fastapi_jwt import (
  JwtAccessBearerCookie,
  JwtAuthorizationCredentials,
  JwtRefreshBearer
)
from jwt_auth import access_security, refresh_security
import pandas as pd
import os

app = APIRouter()

IMAGEDIR = "images/profile"

@app.get('/fotoprofile/{filename}')
def fnProfile(filename: str):
  img_path = os.path.join(IMAGEDIR, filename)
  return FileResponse(img_path, media_type='image/png')

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

@app.post('/register')
async def fnRegis(
  request: Request
) :
  cursor = conn.cursor()

  try:
    data = await request.json()
    username = data['username']
    email = data['email']
    passwd = data['passwd']

    #Cek Email ad atau nd
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email, ))
    itemEmail = cursor.fetchall()

    if len(itemEmail) > 0:
      return JSONResponse(content={"Error": "Email Sudah Terdaftar"}, status_code=409) #code duplicate
    else:
      insQuery = "INSERT INTO users(username, email, passwd) VALUES(%s, %s, %s)"
      cursor.execute(insQuery, (username, email, passwd))
      conn.commit()

      return JSONResponse(content={"Success": "Email Terdaftar"}, status_code=200)


  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()

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
    subject.pop("created_at", None)

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

@app.put('/updateProfile')
async def updateProfile(
  fotoProfile: Optional[UploadFile] = File(None),
  username: str = Form(...),
  email: str = Form(...),
  nohp: str = Form(...),
  jk: bool = Form(...),
  user : JwtAuthorizationCredentials = Security(access_security),

) :
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
        UPDATE users SET username = %s, no_hp = %s, jk = %s
        WHERE id = %s
      """

      cursor.execute(q1, (username, nohp, jk, user['id']))
      conn.commit()
    else:
      filename = f"{uuid.uuid4()}.png"
      file_location = os.path.join(IMAGEDIR, filename)

      #saveFile
      content = await fotoProfile.read()
      with open(file_location, "wb") as f:
        f.write(content)

      q1 = """
        UPDATE users SET username = %s, profile_picture = %s, no_hp = %s, jk = %s
        WHERE id = %s
      """

      cursor.execute(q1, (username, filename, nohp, jk, user['id']))
      conn.commit()

    return JSONResponse(content={"Pesan": "Sukses Update"}, status_code=200)

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  
  finally:
    cursor.close()

@app.put('/changePass')
async def fnChangePass(
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security),
) :
  try:
    cursor = conn.cursor()
    data = await request.json()

    oldPasswd= data['oldPass']
    newPasswd= data['newPass']

    q1 = "SELECT * FROM users WHERE email = %s AND passwd = %s"
    cursor.execute(q1, (user['email'], oldPasswd))

    items = cursor.fetchall()

    if not items:
      return JSONResponse(content={"Error": "Password Lama Tidak Cocok"}, status_code=401)
    
    else:
      q2 = "UPDATE users SET passwd = %s WHERE email = %s"
      cursor.execute(q2, (newPasswd, user['email']))
      conn.commit()

      return JSONResponse(content={"Success": "Password Sudah Diganti"}, status_code=200)

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)

  finally:
    cursor.close()
