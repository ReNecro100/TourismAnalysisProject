#Получить случайные записи (вплоть до 100)
#Cортировка по значениям

#fastapi dev api.py --port 2137
#pip install "fastapi[standart]"

from fastapi import FastAPI
from .routers import cohort, count_sort, general

app = FastAPI()

app.include_router(cohort.router)
app.include_router(count_sort.router)
app.include_router(general.router)
