from fastapi import APIRouter, Depends
from ..dependencies.database import get_dict_cursor

router = APIRouter()

@router.get("/", tags=["Тестовые запросы"])
def read_root():
    return {"message": "Yeah, that's Nizhny Novgorod 2022 Tourists API"}

@router.get("/random_rows/{n}", tags=["Тестовые запросы"])
def get_random_rows(n, cursor = Depends(get_dict_cursor)):
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

def get_cohorting(query, cursor):
    cursor.execute(query)
    data = cursor.fetchall()
    strings = []
    for row in data:
        strings.append({"name": row[0], "avg_days_cnt": row[1], "avg_visitors_cnt": row[2], "avg_spent": row[3]})
    return strings

@router.get("/avg_values", tags=["Средние значения"])
def avg_values(cursor = Depends(get_dict_cursor)):
    return get_cohorting("select 'Все туристы', avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists;", cursor)