#Получить случайные записи (вплоть до 100)
#Cортировка по значениям

#pip install "fastapi[standart]"
#fastapi dev api.py --port 2137

from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Yeah, that's Nizhny Novgorod 2022 Tourists API"}

@app.get("/random_rows/{n}")
def get_random_rows(n):
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432",
    )

    cursor = connection.cursor()
    query = f"""SELECT 
    -- Первичный ключ
    t.index,
    
    -- Прямые поля из Tourists
    t.territory_code,
    t.territory_name,
    t.date_of_arrival,
    
    -- Из справочника trip_type
    tt.name AS trip_type_name,
    
    -- Из справочника visit_type
    vt.name AS visit_type_name,
    
    -- География (3 отдельных справочника, без связей между ними)
    c.name AS home_country_name,
    r.name AS home_region_name,
    ct.name AS home_city_name,
    
    -- Цель поездки
    g.name AS goal_name,
    
    -- Пол
    gen.name AS gender_name,
    
    -- Возрастная группа
    ta.name AS tourist_age_name,
    
    -- Доходная группа
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

-- Опционально: фильтр по одному туристу
-- WHERE t.index = 12345

ORDER BY RANDOM() limit {n};"""
    cursor.execute(query)
    data = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

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

@app.get("/count_sort/{type}")
def get_sorted_by(type: str):
    """
    Get number of rows sorted by type:
    \n /count_sort/month
    \n /count_sort/trip_type
    \n /count_sort/visit_type
    \n /count_sort/goal
    \n /count_sort/gender
    \n /count_sort/tourist_age
    \n /count_sort/income
    \n /count_sort/days_cnt
    \n /count_sort/visitors_cnt
    """
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432",
    )

    cursor = connection.cursor()
    query = ""
    if type == "month":
        query = f"SELECT TO_CHAR(date_of_arrival, 'YYYY-MM') as month, COUNT(*) as total_trips FROM tourists.tourists GROUP BY TO_CHAR(date_of_arrival, 'YYYY-MM') ORDER BY month;"
    elif type == "trip_type":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.trip_type tt on t.trip_type_id=tt.id group by tt.name;"
    elif type == "visit_type":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.visit_type tt on t.visit_type_id=tt.id group by tt.name;"
    elif type == "goal":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.goal tt on t.goal_id=tt.id group by tt.name;"
    elif type == "gender":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.gender tt on t.gender_id=tt.id group by tt.name;"
    elif type == "tourist_age":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.tourist_age tt on t.tourist_age_id=tt.id group by tt.name;"
    elif type == "income":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.income tt on t.income_id=tt.id group by tt.name;"
    elif type == "visitors_cnt":
        query = f"select visitors_cnt, count(*) from tourists.tourists group by visitors_cnt;"
    elif type == "days_cnt":
        query = f"select days_cnt, count(*) from tourists.tourists group by days_cnt;"
    else:
        return {"error": "Wrong type of column"}
    cursor.execute(query)
    data = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    strings = []
    for row in data:
        strings.append({"name": row[0], "count": row[1]})

    return strings

@app.get("/count_sort_geo/{type}")
def get_sorted_by(type: str):
    """
        Get number of rows sorted by type:
        \n /count_sort_geo/home_country
        \n /count_sort_geo/home_region
        \n /count_sort_geo/home_city
        """
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432",
    )

    cursor = connection.cursor()
    query = ""
    if type == "home_country":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.country tt on t.home_country_id=tt.id group by tt.name;"
    elif type == "home_region":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.region tt on t.home_region_id=tt.id group by tt.name;"
    elif type == "home_city":
        query = f"select tt.name, count(*) from tourists.tourists t join tourists.city tt on t.home_city_id=tt.id group by tt.name;"
    else:
        return {"error": "Wrong type of column"}
    cursor.execute(query)
    data = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    strings = []
    for row in data:
        strings.append({"name": row[0], "count": row[1]})

    return strings

@app.get("/cohort_geo/{type}")
def cohort_analytic(type: str):
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432",
    )

    cursor = connection.cursor()
    query = ""
    if type == "home_region":
        query = f"select tt.name, avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists t join tourists.region tt on t.home_region_id=tt.id group by tt.name;"
    elif type == "home_city":
        query = f"select tt.name, avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists t join tourists.city tt on t.home_city_id=tt.id group by tt.name;"
    else:
        return {"error": "Wrong type of column"}
    cursor.execute(query)
    data = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

    strings = []
    for row in data:
        strings.append({"name": row[0], "avg_days_cnt": row[1], "avg_visitors_cnt": row[2], "avg_spent": row[3]})

    return strings