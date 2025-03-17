import psycopg2

def read_config(filename):
  with open(filename, 'r') as file:
    line = file.readline().strip() # Baca baris pertama dan remove leading/trailing whitespace
    if line:
      parts = line.split(",")
      if len(parts) == 5: #cek klo yg udh d split mmg isinya 5
        return tuple(part.strip() for part in parts)
      else:
        print(f"Error: Incorrect number of elements in the line. Expected 5, found {len(parts)}.")
        return None
      
result = read_config('koneksi_config.txt')

if result:
  db_name, host, user, passwd, port = result

  conn = psycopg2.connect(
    database=db_name,
    host=host,
    user=user,
    password=passwd,
    port=port
  )


