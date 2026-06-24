from fastapi import APIRouter, Depends
from ..dependencies.database import get_dict_cursor

router = APIRouter()

def get_cohorting(query, cursor):
    cursor.execute(query)
    data = cursor.fetchall()
    strings = []
    print(data)
    for row in data:
        strings.append({"name": row[0], "avg_days_cnt": row[1], "avg_visitors_cnt": row[2], "avg_spent": row[3]})
    return strings

@router.get("/cohort_geo/home_region", tags=["Когортный анализ"])
def count_sort_region(cursor = Depends(get_dict_cursor)):
    return get_cohorting(f"select tt.name, avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists t join tourists.region tt on t.home_region_id=tt.id group by tt.name;", cursor)

@router.get("/cohort_geo/home_city", tags=["Когортный анализ"])
def count_sort_region(cursor = Depends(get_dict_cursor)):
    return get_cohorting(f"select tt.name, avg(days_cnt), avg(visitors_cnt), avg(spent) from tourists.tourists t join tourists.city tt on t.home_city_id=tt.id group by tt.name;", cursor)