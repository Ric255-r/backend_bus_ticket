from fastapi import FastAPI, File, Form, UploadFile, APIRouter, Request, HTTPException, Security, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi_jwt import (
  JwtAccessBearerCookie,
  JwtAuthorizationCredentials,
  JwtRefreshBearer
)
from router.routeAdmin import idPaket

import pandas as pd
from jwt_auth import access_security
from koneksi import conn
import os
import uuid
from datetime import datetime
from typing import Optional, Union
from utils.fnConvertStr import serialize_data

app = APIRouter()

IMAGEDIR = "images/buktiByr/"

@app.get('/buktiByr/{filename}')
def fnBuktiByr(filename: str):
  img_path = os.path.join(IMAGEDIR, filename)
  return FileResponse(img_path, media_type='image/png')

@app.get('/fotoPaket/{filename}')
def fnGbrPaket(filename: str):
  img_path = os.path.join("images/gbrpaket", filename)
  return FileResponse(img_path, media_type='image/png')

@app.get('/fotoLogoBis/{filename}')
def fnLogoBis(filename: str):
  img_path = os.path.join("images/logoBis", filename)
  return FileResponse(img_path, media_type='image/png')

@app.get('/fotoGbrBis/{filename}')
def fnGbrBis(filename: str):
  img_path = os.path.join("images/gbrbis", filename)
  return FileResponse(img_path, media_type='image/png')

def getLastTrans():
  """
    TEST QUERY UNTUK CHECKOUT
    QUERY 1
    SELECT t.*, JSON_AGG(
      jsonb_build_object(
        'id_trans', dt.id_trans,
        'id_bis', dt.id_bis,
        'tgl_pergi', dt.tgl_pergi,
        'tgl_balik', dt.tgl_balik,
        'jlh_penumpang', dt.jlh_penumpang,
        'hrg_tiket', dt.hrg_tiket_penumpang
      )
    ) AS detailTrans, b.*, kb.* FROM transaksi t
      RIGHT JOIN "detailTransaksi" dt ON t.id_trans = dt.id_trans
      LEFT JOIN bis b ON dt.id_bis = b.id_bis
      LEFT JOIN kelas_bis kb ON b.id_kelas_bis = kb.id_kelas
      INNER JOIN rute r ON b.id_rute = r.id
      GROUP BY t.id_trans, b.id_bis, kb.id_kelas

    QUERY 2
    SELECT t.*, dt.*, b.*, kb.* FROM transaksi t
    LEFT JOIN "detailTransaksi" dt ON t.id_trans = dt.id_trans
    LEFT JOIN bis b ON dt.id_bis = b.id_bis
    LEFT JOIN kelas_bis kb ON b.id_kelas_bis = kb.id_kelas
    INNER JOIN rute r ON b.id_rute = r.id
  """
  cursor = conn.cursor()
  try:
    query = "SELECT * FROM transaksi ORDER BY id_trans DESC"
    cursor.execute(query)
    result = cursor.fetchone() # ini return value dari db, dalam bentuk array.
    id_trans = result[0] if result is not None else None

    if id_trans is None:
      num = "1"
      strpad = "A" + num.zfill(4)
    else:
      getNum = id_trans[1:5]  # ambil angka dari index ke 1 sampai index ke 5
      num = int(getNum) + 1
      strpad = "A" + str(num).zfill(4)

    return strpad
  finally:
    cursor.close()

@app.get('/listbis')
async def getListBis(
  id_bis: Optional[str] = Query(None)
):
  cursor = conn.cursor()
  try:
    query = f"""
      SELECT b.*, kb.*, r.* from bis b 
      LEFT JOIN kelas_bis kb ON b.id_kelas_bis = kb.id_kelas
      LEFT JOIN rute r ON b.id_rute = r.id 
      {'WHERE b.id_bis = %s' if id_bis is not None else ""}
    """

    if id_bis is not None:
      cursor.execute(query, (id_bis, ))
    else:
      cursor.execute(query)

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])

    items = cursor.fetchall()

    if not items:
      return items
    else:
      df = pd.DataFrame(items, columns=column_name)
      return df.to_dict('records')
    
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()

@app.get('/listbis/{nama_bis}')
async def listBisParameter(nama_bis: Optional[str] = None):
  cursor = conn.cursor()
  try:
    kondisi = ""
    if nama_bis is not None:
      kondisi = f"WHERE b.nama_bis LIKE '%{nama_bis.upper()}%'"

    query = f"""
      SELECT b.*, kb.*, r.* from bis b 
      LEFT JOIN kelas_bis kb ON b.id_kelas_bis = kb.id_kelas
      LEFT JOIN rute r ON b.id_rute = r.id {kondisi}
    """

    cursor.execute(query)

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])

    items = cursor.fetchall()

    if not items:
      return items
    else:
      df = pd.DataFrame(items, columns=column_name)
      return df.to_dict('records')
    
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()



# Note Kalo Error
# ValueError: Out of range float values are not JSON compliant
# Langsung hajar konversi ke string aja.

@app.get('/cekpaket')
async def getIsiPaket(
  id_paket: Optional[str] = Query(None)
):
  cursor = conn.cursor()
  try:
    query = f"""
      SELECT 
        p.*, b.nama_bis, b.id_rute,
        COALESCE( 
          json_agg(
            jsonb_build_object(
              'id_benefit', bw.id_benefit,
              'benefit', bw.benefit
            )
          ) FILTER (WHERE bw.id_benefit IS NOT NULL), 
          '[]'::json
        ) AS detailpaket
      FROM 
        paketwisata p
      LEFT JOIN 
        benefitwisata bw ON p.id_benefit = bw.id_benefit
      LEFT JOIN 
        bis b ON p.id_bis = b.id_bis
      {'WHERE p.id_paket = %s' if id_paket is not None else ""}
      GROUP BY 
        p.id_paket, b.nama_bis, b.id_rute;
    """
    if id_paket is not None:
      cursor.execute(query, (id_paket, ))
    else: 
      cursor.execute(query)

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])

    items = serialize_data(cursor.fetchall())

    df = pd.DataFrame(items, columns=column_name)
    data = df.to_dict('records')

    return data
  
  except HTTPException as e:
  
    print(e)
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  except ValueError as e:
    print(f"Error occurred: {e}")
 
  finally:
    cursor.close()

@app.get('/kota')
async def getKota():
  cursor = conn.cursor()
  try:
    # Query Awal. diganti karena merasa tidak guna
    # query = "SELECT * FROM kota"
    # cursor.execute(query)
    query = """
      SELECT kota_awal AS nama_kota FROM rute 
      UNION SELECT kota_akhir FROM rute
    """
    cursor.execute(query)

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])

    items = cursor.fetchall()

    if not items:
      return items
    else:
      df = pd.DataFrame(items, columns=column_name)
      isiData = df.to_dict('records') #get seluruh data tanpa panggil index
      return isiData
    
  except HTTPException as e:
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  finally:
    cursor.close()

@app.get('/checkout')
async def getTransaksi(
  status: Optional[str] = Query(None), # Untuk ambil queryString
  user: JwtAuthorizationCredentials = Security(access_security),
):
  cursor = conn.cursor()
  # kalo ad error object nontype is non subscriptable. itu logout
  try:
    if status is not None:
      query = """
        SELECT t.*, dt.tgl_pergi, dt.tgl_balik, b.id_rute,
        b.jasa_travel, pw.nama_paket, pw.gbrpaket FROM transaksi t 
        INNER JOIN "detailTransaksi" dt ON t.id_trans = dt.id_trans
        INNER JOIN bis b ON dt.id_bis = b.id_bis
        LEFT JOIN paketwisata pw ON t.id_paket = pw.id_paket
        WHERE t.email_cust = %s AND t.status_trans = %s ORDER BY t.tgl_trans DESC
      """

      cursor.execute(query, (user['email'], status.upper()))
    else:
      query = """
        SELECT t.*, pw.nama_paket, b.jasa_travel FROM transaksi t
        LEFT JOIN paketwisata pw ON t.id_paket = pw.id_paket
        INNER JOIN "detailTransaksi" dt ON t.id_trans = dt.id_trans
        INNER JOIN bis b ON dt.id_bis = b.id_bis
        WHERE t.email_cust = %s ORDER BY t.tgl_trans DESC

      """
      cursor.execute(query, (user['email'], ))

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])
    
    items = cursor.fetchall()

    # cek array items kosong atau nda
    if(not items):
      return items
    else:
      subject = pd.DataFrame(items, columns=column_name)
      return subject.to_dict('records')[0] if status is None else subject.to_dict('records')  #index 0 ini kalau cmn mw ambil 1 data

  except HTTPException as e:
    # print(cursor.description)
    # print(status)
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  
  finally:
    cursor.close()

@app.get('/checkout/{id_trans}')
async def getTransaksi(
  id_trans: str,
  user: JwtAuthorizationCredentials = Security(access_security),
):
  cursor = conn.cursor()
  # kalo ad error object nontype is non subscriptable. itu logout
  try:
    query = """
      SELECT t.*, dt.tgl_pergi, dt.tgl_balik, dt.jlh_penumpang, dt.hrg_tiket_perorg, b.jasa_travel,
      b.nama_bis, kb.nama_kelas, r.kota_awal, r.kota_akhir, kb.harga, r.waktu_berangkat, r.waktu_sampai
      FROM transaksi t
      INNER JOIN "detailTransaksi" dt ON t.id_trans = dt.id_trans
      INNER JOIN bis b ON dt.id_bis = b.id_bis
      INNER JOIN kelas_bis kb ON b.id_kelas_bis = kb.id_kelas
      INNER JOIN rute r ON b.id_rute = r.id
      WHERE t.email_cust = %s AND t.id_trans = %s
      LIMIT 1
    """
    #query = "SELECT * FROM transaksi WHERE email_cust = %s AND id_trans = %s ORDER BY tgl_trans DESC"
    cursor.execute(query, (user['email'], id_trans))

    column_name = []
    for kol in cursor.description:
      column_name.append(kol[0])
    
    items = cursor.fetchall()

    # cek array items kosong atau nda
    if(not items):
      return items
    else:
      subject = pd.DataFrame(items, columns=column_name)
      return subject.to_dict('records')[0]  #index 0 ini kalau cmn mw ambil 1 data

  except HTTPException as e:
    # print(cursor.description)
    # print(status)
    return JSONResponse(content={"Error": str(e)}, status_code=e.status_code)
  
  finally:
    cursor.close()
    
#Khusus untuk formData. untuk field isian, declare variable sebagai parameter fungsi
@app.post('/checkout')
async def bayar(
  buktiByr: Optional[UploadFile] = File(None),
  user: JwtAuthorizationCredentials = Security(access_security),
  id_bis: str = Form(...),
  tgl_pergi: str = Form(...),
  tgl_balik: str = Form(...),
  jlh_penumpang: int = Form(...),
  hrg_tiket_perorg: float = Form(...),
  total_harga: float = Form(...),
  id_paket: Optional[str] = Form(None)
):
  # Note kalo error not all arguments converted during string formatting.
  # itu bs jadi kurang kolom, kurang value, atau kurang %s di query sql
  id_trans = getLastTrans()
  try:
    cursor = conn.cursor()
    # Ensure directory exists
    if not os.path.exists(IMAGEDIR):
        os.makedirs(IMAGEDIR)

    qCekTiket = """
      SELECT tiket_tersedia FROM stok_tiket WHERE id_bis = %s
    """
    cursor.execute(qCekTiket, (id_bis, ))
    result = cursor.fetchone()

    if result is None:
      raise HTTPException(status_code=404, detail="Bus not found")
  
    tiket_tersedia = result[0]

    # Check if bukti bayar kosong. ini byr cash
    if not buktiByr:
      # Update Stok Tiket 
      # if available_tickets >= number_of_tickets:

      qTiket = """
        UPDATE stok_tiket SET tiket_tersedia = tiket_tersedia - %s WHERE id_bis = %s
      """
      cursor.execute(qTiket, (jlh_penumpang, id_bis))
      conn.commit()

      if id_paket is None:
        # query 
        q1 = """
          INSERT INTO transaksi(id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr) 
          values(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q1, (id_trans, 'nofoto', datetime.now(), user['email'], 'ST001', 'PENDING', total_harga, 'cash') )
        conn.commit()
        
        #q2 untuk detailTrans. mesti pake triplequotes soalny nama tabel ak camelcase.
        q2 = """
          INSERT INTO "detailTransaksi"(id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg)
          VALUES(%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q2, (id_trans, id_bis, tgl_pergi, tgl_pergi if tgl_balik == "" else tgl_balik, jlh_penumpang, hrg_tiket_perorg))
        conn.commit()

        #return {"message": "Transaksi Cash Oke"}
      # raise HTTPException(status_code=400, detail="No file provided")
      else:
        
        # Jika Psn Lwt Paket
        q1 = """
          INSERT INTO transaksi(id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket) 
          values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q1, (id_trans, 'nofoto', datetime.now(), user['email'], 'ST001', 'PENDING', total_harga, 'cash', id_paket) )
        conn.commit()
        
        #q2 untuk detailTrans. mesti pake triplequotes soalny nama tabel ak camelcase.
        q2 = """
          INSERT INTO "detailTransaksi"(id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg)
          VALUES(%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q2, (id_trans, id_bis, tgl_pergi, tgl_pergi if tgl_balik == "" else tgl_balik, jlh_penumpang, hrg_tiket_perorg))
        conn.commit()

        #return {"message": "Transaksi Cash Oke"}

    else:
      # Update Stok Tiket 
      # if available_tickets >= number_of_tickets:

      qTiket = """
        UPDATE stok_tiket SET tiket_tersedia = tiket_tersedia - %s WHERE id_bis = %s
      """
      cursor.execute(qTiket, (jlh_penumpang, id_bis))
      conn.commit()

      # Kondisi kalo checkout tanpa paket.
      if id_paket is None:
        # kondisi kalo bukti bayar ga kosong
        # Create a unique filename
        filename = f"{uuid.uuid4()}.jpg"
        file_location = os.path.join(IMAGEDIR, filename)

        # Read and save the file
        content = await buktiByr.read()
        with open(file_location, "wb") as f:
            f.write(content)
        
        # query 
        q1 = """
          INSERT INTO transaksi(id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr) 
          values(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q1, (id_trans, filename, datetime.now(), user['email'], 'ST001', 'PENDING', total_harga, 'transfer') )
        conn.commit()
        
        #q2 untuk detailTrans. mesti pake triplequotes soalny nama tabel ak camelcase.
        q2 = """
          INSERT INTO "detailTransaksi"(id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg)
          VALUES(%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q2, (id_trans, id_bis, tgl_pergi, tgl_pergi if tgl_balik == "" else tgl_balik, jlh_penumpang, hrg_tiket_perorg))
        conn.commit()

        #return {"message": "File uploaded successfully", "filename": filename}
      else:
        # kondisi kalo bukti bayar ga kosong
        # Create a unique filename
        filename = f"{uuid.uuid4()}.jpg"
        file_location = os.path.join(IMAGEDIR, filename)

        # Read and save the file
        content = await buktiByr.read()
        with open(file_location, "wb") as f:
            f.write(content)
        
        # query 
        q1 = """
          INSERT INTO transaksi(id_trans, bukti_foto, tgl_trans, email_cust, id_staff, status_trans, total_harga, metode_byr, id_paket) 
          values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q1, (id_trans, filename, datetime.now(), user['email'], 'ST001', 'PENDING', total_harga, 'transfer', id_paket) )
        conn.commit()
        
        #q2 untuk detailTrans. mesti pake triplequotes soalny nama tabel ak camelcase.
        q2 = """
          INSERT INTO "detailTransaksi"(id_trans, id_bis, tgl_pergi, tgl_balik, jlh_penumpang, hrg_tiket_perorg)
          VALUES(%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(q2, (id_trans, id_bis, tgl_pergi, tgl_pergi if tgl_balik == "" else tgl_balik, jlh_penumpang, hrg_tiket_perorg))
        conn.commit()

        #return {"message": "File uploaded successfully", "filename": filename}


    return JSONResponse(content={"Pesan": "Transaksi Sukses"}, status_code=200)
  except Exception as e:
    print(str(e))
    raise HTTPException(status_code=500, detail=str(e))
  
  finally: 
    cursor.close()