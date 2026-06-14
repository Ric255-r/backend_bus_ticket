import psycopg2

from app.core.config import DB_CONFIG


conn = psycopg2.connect(**DB_CONFIG)
