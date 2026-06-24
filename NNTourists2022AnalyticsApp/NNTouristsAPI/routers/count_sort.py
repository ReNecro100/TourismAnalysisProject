from fastapi import APIRouter, Depends
from ..dependencies.database import get_dict_cursor

router = APIRouter()

@router.get("/count_sort/month", tags=["Сортировка по столбцу"])
def count_sort_month(cursor = Depends(get_dict_cursor)):
    query = f"SELECT TO_CHAR(date_of_arrival, 'YYYY-MM') as month, COUNT(*) as total_trips, avg(spent)*1000000 FROM tourists.tourists GROUP BY TO_CHAR(date_of_arrival, 'YYYY-MM') ORDER BY month;"
    cursor.execute(query)
    data = cursor.fetchall()
    strings = []
    for row in data:
        strings.append({"name": row[0], "count": row[1], "average": row[2]})
    return strings

def get_sortings(query, cursor):
    cursor.execute(query)
    data = cursor.fetchall()
    strings = []
    for row in data:
        strings.append({"name": row[0], "count": row[1]})
    return strings

@router.get("/count_sort/trip_type", tags=["Сортировка по столбцу"])
def count_sort_trip_type(cursor = Depends(get_dict_cursor)):
    return get_sortings("select tt.name, count(*) from tourists.tourists t join tourists.trip_type tt on t.trip_type_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort/visit_type", tags=["Сортировка по столбцу"])
def count_sort_visit_type(cursor = Depends(get_dict_cursor)):
    return get_sortings("select tt.name, count(*) from tourists.tourists t join tourists.visit_type tt on t.visit_type_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort/goal", tags=["Сортировка по столбцу"])
def count_sort_goal(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.goal tt on t.goal_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort/gender", tags=["Сортировка по столбцу"])
def count_sort_gender(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.gender tt on t.gender_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort/tourist_age", tags=["Сортировка по столбцу"])
def count_sort_tourist_age(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.tourist_age tt on t.tourist_age_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort/income", tags=["Сортировка по столбцу"])
def count_sort_income(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.income tt on t.income_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort/visitors_cnt", tags=["Сортировка по столбцу"])
def count_sort_visitors_cnt(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select visitors_cnt, count(*) from tourists.tourists group by visitors_cnt;", cursor)

@router.get("/count_sort/days_cnt", tags=["Сортировка по столбцу"])
def count_sort_days_cnt(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select days_cnt, count(*) from tourists.tourists group by days_cnt;", cursor)

@router.get("/count_sort_geo/home_country", tags=["Сортировка по столбцу"])
def count_sort_country(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.country tt on t.home_country_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort_geo/home_region", tags=["Сортировка по столбцу"])
def count_sort_region(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.region tt on t.home_region_id=tt.id group by tt.name;", cursor)

@router.get("/count_sort_geo/home_city", tags=["Сортировка по столбцу"])
def count_sort_region(cursor = Depends(get_dict_cursor)):
    return get_sortings(f"select tt.name, count(*) from tourists.tourists t join tourists.city tt on t.home_city_id=tt.id group by tt.name;", cursor)