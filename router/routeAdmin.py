from fastapi import FastAPI, File, Form, UploadFile, APIRouter, Request, HTTPException, Security, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi_jwt import (
  JwtAccessBearerCookie,
  JwtAuthorizationCredentials,
  JwtRefreshBearer
)
import pandas as pd
from jwt_auth import access_security
from koneksi import conn
import os
import uuid
from datetime import datetime
from typing import Optional, Union

app = APIRouter()


#Bagian Rute
@app.get('/rute')
async def getRute(
  id_rute: Optional[str] = Query(None),
  user: JwtAuthorizationCredentials = Security(access_security)
):
  try:
    cursor = conn.cursor()
    if id_rute is None:
      q1 = "SELECT * FROM rute"
      cursor.execute(q1)
    else:
      q1 = "SELECT * FROM rute WHERE id = %s"
      cursor.execute(q1, (id_rute, ))

    items = cursor.fetchall()

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])

    df = pd.DataFrame(items, columns=column_name)
    return df.to_dict('records')

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  
  finally:
    cursor.close()

@app.post('/insertRute')
async def insertRute(
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  try:
    cursor = conn.cursor()
    data = await request.json()

    id = data['id']
    kotaAwal = data['kota_awal']
    kotaAkhir = data['kota_akhir']
    waktuBrkt = data['waktu_berangkat']
    waktuSampai = data['waktu_sampai']
    lamaTempuh = data['lama_tempuh_jam']

    q1 = """
      INSERT INTO rute VALUES(%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(q1, (id, kotaAwal, kotaAkhir, lamaTempuh, waktuBrkt, waktuSampai))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Tersimpan"}, status_code=200)
  
  except HTTPException as e:
    return JSONResponse(content={"Error": "Dat tdk simpan"}, status_code=e.status_code)
  finally:
    cursor.close()

@app.put('/editRoute/{id}')
async def editRute(
  id: str,
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  try:
    cursor = conn.cursor()
    data = await request.json()

    kotaAwal = data['kota_awal']
    kotaAkhir = data['kota_akhir']
    waktuBrkt = data['waktu_berangkat']
    waktuSampai = data['waktu_sampai']
    lamaTempuh = data['lama_tempuh_jam']

    q1 = """
      UPDATE rute SET kota_awal = %s, kota_akhir = %s, waktu_berangkat = %s, waktu_sampai = %s, lama_tempuh_jam = %s
      WHERE id = %s
    """
    cursor.execute(q1, (kotaAwal, kotaAkhir, waktuBrkt, waktuSampai, lamaTempuh, id))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Tersimpan"}, status_code=200)
  
  except HTTPException as e:
    return JSONResponse(content={"Error": "Dat tdk simpan"}, status_code=e.status_code)
  finally:
    cursor.close()


@app.delete('/rute/{id}')
async def deleteRute(
  id: str,
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  try:
    cursor = conn.cursor()

    q1 = """
      DELETE FROM rute WHERE id = %s
    """
    cursor.execute(q1, (id, ))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Kehapus"}, status_code=200)
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()
#End Bagian Rute

#yang getnya ada di ruteTransaksi.py
#Start bagian insertBis
@app.post('/insertBis')
async def insertBis(
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security)
):
  try:
    cursor = conn.cursor()

    data = await request.json()

    id = data['id_bis']
    namaBis = data['nama_bis']
    idKelasBis = data['id_kelas_bis']
    jasaTravel = data['jasa_travel']
    idRute = data['id_rute']

    q1 = """
      INSERT INTO bis VALUES(%s, %s, %s, %s, %s)
    """
    cursor.execute(q1, (id, namaBis, idKelasBis, jasaTravel, idRute))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Tersimpan"}, status_code=200)
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()

@app.put('/updateBis/{id}')
async def updateBis(
  id:str,
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security)
):
  try:
    cursor = conn.cursor()

    data = await request.json()

    namaBis = data['nama_bis']
    idKelasBis = data['id_kelas_bis']
    jasaTravel = data['jasa_travel']
    idRute = data['id_rute']

    q1 = """
      UPDATE bis SET nama_bis = %s, id_kelas_bis = %s, jasa_travel = %s, id_rute = %s
      WHERE id_bis = %s
    """
    cursor.execute(q1, (namaBis, idKelasBis, jasaTravel, idRute, id))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Tersimpan"}, status_code=200)
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()

@app.delete('/listbis/{id}')
async def deleteBis(
  id: str,
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  try:
    cursor = conn.cursor()

    q1 = """
      DELETE FROM bis WHERE id_bis = %s
    """
    cursor.execute(q1, (id, ))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Kehapus"}, status_code=200)
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()
#End Bagian insertBis


#Start Bagian Kelas Bis
@app.get('/kelasbis')
async def getKelasBis(
  id_kelas: Optional[str] = Query(None)
):
  try:
    if id_kelas is None:
      cursor = conn.cursor()
      q1 = "SELECT * FROM kelas_bis"
      cursor.execute(q1)
    else:
      cursor = conn.cursor()
      q1 = "SELECT * FROM kelas_bis WHERE id_kelas = %s"
      cursor.execute(q1, (id_kelas, ))

    items = cursor.fetchall()

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])

    df = pd.DataFrame(items, columns=column_name)
    return df.to_dict('records')

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  
  finally:
    cursor.close()

@app.put('/kelasbis/{id}')
async def updateKelasBis(
  id:str,
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security)
):
  try:
    cursor = conn.cursor()

    data = await request.json()

    dt1 = data['nama_kelas']
    dt2 = data['harga']

    q1 = """
      UPDATE kelas_bis SET nama_kelas = %s, harga = %s
      WHERE id_kelas = %s
    """
    cursor.execute(q1, (dt1, dt2, id))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Tersimpan"}, status_code=200)
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()


@app.post('/kelasbis')
async def insertKelasBis(
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security)
):
  try:
    cursor = conn.cursor()

    data = await request.json()

    id = data['id_kelas']
    dt1 = data['nama_kelas']
    dt2 = data['harga']

    q1 = """
      INSERT INTO kelas_bis VALUES(%s, %s, %s)
    """
    cursor.execute(q1, (id, dt1, dt2))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Tersimpan"}, status_code=200)
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()

@app.delete('/kelasbis/{id}')
async def deleteKelasBis(
  id: str,
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  try:
    cursor = conn.cursor()

    q1 = """
      DELETE FROM kelas_bis WHERE id_kelas = %s
    """
    cursor.execute(q1, (id, ))
    conn.commit()

    return JSONResponse(content={"Success": "Dat Kehapus"}, status_code=200)
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()
#End Bagian KelasBis

# Start Transaksi
@app.get('/dataTrans')
async def getAllTrans(
  id: Optional[str] = Query(None), # Untuk ambil queryString
  user: JwtAuthorizationCredentials = Security(access_security)
):
  if user['roles'] == "ADMIN":
    try:
      cursor = conn.cursor()

      if id is not None:
        q1 = """
            SELECT t.*, u.*, dt.id_bis, dt.tgl_pergi, dt.jlh_penumpang, dt.tgl_balik, 
            b.id_rute, b.nama_bis, b.id_kelas_bis, pw.nama_paket, r.kota_awal, r.kota_akhir FROM transaksi t 
            INNER JOIN "detailTransaksi" dt ON t.id_trans = dt.id_trans
            INNER JOIN bis b ON dt.id_bis = b.id_bis
            INNER JOIN users u ON t.email_cust = u.email
            LEFT JOIN rute r ON b.id_rute = r.id
            LEFT JOIN paketwisata pw ON t.id_paket = pw.id_paket
            WHERE t.id_trans = %s
        """
        cursor.execute(q1, (id, )) #kalo tuple sifatnya gini. klo data single kasih 1 koma ksg
      else:
        q1 = """
            SELECT t.*, dt.tgl_pergi, dt.tgl_balik, b.id_rute, pw.nama_paket FROM transaksi t 
            INNER JOIN "detailTransaksi" dt ON t.id_trans = dt.id_trans
            INNER JOIN bis b ON dt.id_bis = b.id_bis
            LEFT JOIN paketwisata pw ON t.id_paket = pw.id_paket
        """
        cursor.execute(q1)


      column_name = []
      for kol in cursor.description:
        column_name.append(kol[0])
      
      items = cursor.fetchall()

      df = pd.DataFrame(items, columns=column_name)

      data = df.to_dict('records')
      return data

    except HTTPException as e:
      return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
    
    finally:
      cursor.close()
  else:
    return JSONResponse(content={"Error": "Unauhorized"}, status_code=401)


@app.put('/dataTrans/{id}')
async def updateTrans(
  id: str,
  request: Request,
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  try:
    cursor = conn.cursor()
    data = await request.json()
    # print(data)

    if data['status_trans'] == "CANCELLED":
      q1 = "UPDATE transaksi SET status_trans = %s, alasan_tolak = %s WHERE id_trans = %s"
      cursor.execute(q1, (data['status_trans'], data['alasan_tolak'], id))
    else:
      q1 = "UPDATE transaksi SET status_trans = %s WHERE id_trans = %s"
      cursor.execute(q1, (data['status_trans'], id))

    conn.commit()

    return JSONResponse(content=data, status_code=200)

  except HTTPException as e:
    return JSONResponse(content={"ErrorWoi": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()


@app.delete('/dataTrans/{id}')
async def updateTrans(
  id: str,
  user: JwtAuthorizationCredentials = Security(access_security)
) :
  try:
    cursor = conn.cursor()
    # print(data)

    q1 = "DELETE FROM transaksi WHERE id_trans = %s"
    cursor.execute(q1, (id, ))
    conn.commit()

    return JSONResponse(content={"Success": "Lala"}, status_code=200)

  except HTTPException as e:
    return JSONResponse(content={"ErrorWoi": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()


#End Transaksi
  
  
# Paket
def idPaket():
  try:
    cursor = conn.cursor()
    q1 = "SELECT id_paket FROM paketwisata ORDER BY id_paket DESC LIMIT 1"
    cursor.execute(q1)

    id_awal = cursor.fetchone() #ini haslnya bentuk array. di pecahkan dlu

    if len(id_awal) == 0:
      keyword = "P0001"
      return keyword
    else:
      idAwalToStr = id_awal[0]
      substrIdAwal = idAwalToStr[1:5] #ambil str di index 1, sampai ke "karakter ke 5"
      toIntId = int(substrIdAwal) + 1
      keyword = "P" + str(toIntId).zfill(4) #semacam padleft, dia nambahin zero didepan.
      return keyword
    

  except Exception as e:
    print(e)
  finally:
    cursor.close()

@app.post('/insertPaket')
async def isiPaket(
  request: Request,
  user : JwtAuthorizationCredentials = Security(access_security),
):
  try:
    cursor = conn.cursor()

    form_data = await request.form()

    nama_paket = form_data.get('nama_paket')
    subjudul_paket = form_data.get('subjudul_paket')
    harga_paket = form_data.get('harga_paket')
    id_bis = form_data.get('id_bis')
    id_rute = form_data.get('id_rute')
    tgl_brkt = form_data.get('tgl_brkt')
    tgl_balik = form_data.get('tgl_balik')
    jambrkt = form_data.get('jambrkt')
    jambalik = form_data.get('jambalik')
    jlhpenumpang = form_data.get('jlhpenumpang')
    gbrpaket: Optional[UploadFile] = form_data.get('gbrpaket')
    buatId = idPaket()

    q1 = "SELECT * FROM rute WHERE id = %s"
    cursor.execute(q1, (id_rute, ))
    items = cursor.fetchone()
    print(items)

    q2 = """
      INSERT INTO paketwisata(
        id_paket, nama_paket, harga_paket, id_bis, 
        rute_awal, rute_akhir, tgl_brkt, tgl_balik, 
        gbrpaket, subjudulpaket, jambrkt, jambalik,
        jlhpenumpang
      ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(q2, 
      (buatId, nama_paket, harga_paket, id_bis, items[1], items[2], 
       tgl_brkt, tgl_balik, '', subjudul_paket, jambrkt, jambalik, jlhpenumpang)
    )
    conn.commit()

  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  
  finally:
    cursor.close()



  
  

