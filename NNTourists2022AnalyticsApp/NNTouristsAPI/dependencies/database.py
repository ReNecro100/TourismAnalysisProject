import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import os

# Создаём пул соединений при первом импорте
db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "postgres"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    port=os.getenv("DB_PORT", "5432")
)

@contextmanager
def get_db_connection():
    """Контекстный менеджер для работы с БД"""
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

def get_cursor():
    """Генератор для FastAPI Depends"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            yield cursor

def get_dict_cursor():
    """Генератор для FastAPI Depends (с RealDictCursor)"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            yield cursor