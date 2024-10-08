import psycopg2

conn = psycopg2.connect(
  database="db_bushub",
  host="localhost",
  user="postgres",
  password="1234",
  port="5432"
)
