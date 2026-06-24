#Получить случайные записи (вплоть до 100)
#Cортировка по значениям

#fastapi dev api.py --port 2137
#pip install "fastapi[standart]"

from fastapi import FastAPI
from contextlib import contextmanager
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

db_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "postgres"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    port=os.getenv("DB_PORT", "5432")
)

app = FastAPI()

@contextmanager
def get_db_connection():
    """Берёт соединение из пула и возвращает его обратно после использования"""
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

@app.on_event("shutdown")
def shutdown():
    db_pool.closeall()

@app.get("/", tags=["Тестовые запросы"])
def read_root():
    return {"message": "Yeah, that's Nizhny Novgorod 2022 Tourists API"}

@app.get("/random_rows/{n}", tags=["Тестовые запросы"])
def get_random_rows(n):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = f"""SELECT 
    t.index,
    t.territory_code,
    t.territory_name,
    t.date_of_arrival,
    tt.name AS trip_type_name,
    vt.name AS visit_type_name,
    c.name AS home_country_name,
    r.name AS home_region_name,
    ct.name AS home_city_name,
    g.name AS goal_name,
    gen.name AS gender_name,
    ta.name AS tourist_age_name,
    inc.name AS income_name,
    t.days_cnt,
    t.visitors_cnt,
    t.spent
FROM tourists.tourists t
LEFT JOIN tourists.trip_type tt ON t.trip_type_id = tt.id
LEFT JOIN tourists.visit_type vt ON t.visit_type_id = vt.id
LEFT JOIN tourists.country c ON t.home_country_id = c.id
LEFT JOIN tourists.region r ON t.home_region_id = r.id
LEFT JOIN tourists.city ct ON t.home_city_id = ct.id
LEFT JOIN tourists.goal g ON t.goal_id = g.id
LEFT JOIN tourists.gender gen ON t.gender_id = gen.id
LEFT JOIN tourists.tourist_age ta ON t.tourist_age_id = ta.id
LEFT JOIN tourists.income inc ON t.income_id = inc.id
ORDER BY RANDOM()
LIMIT {n};"""
            cursor.execute(query)
            data = cursor.fetchall()

    strings = []
    for row in data:
        strings.append({
            "index": row[0],
            "territory_code": row[1],
            "territory_name": row[2],
            "date_of_arrival": row[3],
            "trip_type": row[4],
            "visit_type": row[5],
            "home_country": row[6],
            "home_region": row[7],
            "home_city": row[8],
            "goal": row[9],
            "gender": row[10],
            "tourist_age": row[11],
            "income": row[12],
            "days_cnt": row[13],
            "visitors_cnt": row[14],
            "spent": row[15]
        })
    return strings

@app.get("/count_sort/month", tags=["Сортировка по столбцу"])
def count_sort_month():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = f"SELECT TO_CHAR(date_of_arrival, 'YYYY-MM') as month, COUNT(*) as total_trips, avg(spent)*1000000 FROM tourists.tourists GROUP BY TO_CHAR(date_of_arrival, 'YYYY-MM') ORDER BY month;"
            cursor.execute(query)
            data = cursor.fetchall()
    strings = []
    for row in data:
        strings.append({"name": row[0], "count": row[1], "average": row[2]})
    return strings

def get_sortings(query):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
    strings = []
    for row in data:
        strings.append({"name": row[0], "count": row[1]})
    return strings

@app.get("/count_sort/trip_type", tags=["Сортировка по столбцу"])
def count_sort_trip_type():
    return get_sortings("select tt.name, count(*) from tourists.tourists t join tourists.trip_type tt on t.trip_type_id=tt.id group by tt.name;")

@app.get("/count_sort/visit_type", tags=["Сортировка по столбцу"])
def count_sort_visit_type():
    return get_sortings("select tt.name, count(*) from tourists.tourists t join tourists.visit_type tt on t.visit_type_id=tt.id group by tt.name;")

@app.get("/count_sort/goal", tags=["Сортировка по столбцу"])
def count_sort_goal():
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.goal tt on t.goal_id=tt.id group by tt.name;")

@app.get("/count_sort/gender", tags=["Сортировка по столбцу"])
def count_sort_gender():
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.gender tt on t.gender_id=tt.id group by tt.name;")

@app.get("/count_sort/tourist_age", tags=["Сортировка по столбцу"])
def count_sort_tourist_age():
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.tourist_age tt on t.tourist_age_id=tt.id group by tt.name;")

@app.get("/count_sort/income", tags=["Сортировка по столбцу"])
def count_sort_income():
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.income tt on t.income_id=tt.id group by tt.name;")

@app.get("/count_sort/visitors_cnt", tags=["Сортировка по столбцу"])
def count_sort_visitors_cnt():
    return get_sortings(f"select visitors_cnt, count(*) from tourists.tourists group by visitors_cnt;")

@app.get("/count_sort/days_cnt", tags=["Сортировка по столбцу"])
def count_sort_days_cnt():
    return get_sortings(f"select days_cnt, count(*) from tourists.tourists group by days_cnt;")

@app.get("/count_sort_geo/home_country", tags=["Сортировка по столбцу"])
def count_sort_country():
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.country tt on t.home_country_id=tt.id group by tt.name;")

@app.get("/count_sort_geo/home_region", tags=["Сортировка по столбцу"])
def count_sort_region():
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.region tt on t.home_region_id=tt.id group by tt.name;")

@app.get("/count_sort_geo/home_city", tags=["Сортировка по столбцу"])
def count_sort_region():
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.city tt on t.home_city_id=tt.id group by tt.name;")

def get_cohorting(query):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
    strings = []
    for row in data:
        strings.append({"name": row[0], "avg_days_cnt": row[1], "avg_visitors_cnt": row[2], "avg_spent": row[3]})
    return strings
@app.get("/avg_values", tags=["Средние значения"])
def avg_values():
    return get_cohorting("select 'Все туристы', avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists;")

@app.get("/cohort_geo/home_region", tags=["Когортный анализ"])
def count_sort_region():
    return get_cohorting(f"select tt.name, avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists t join tourists.region tt on t.home_region_id=tt.id group by tt.name;")

@app.get("/cohort_geo/home_city", tags=["Когортный анализ"])
def count_sort_region():
    return get_cohorting(f"select tt.name, avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists t join tourists.city tt on t.home_city_id=tt.id group by tt.name;")