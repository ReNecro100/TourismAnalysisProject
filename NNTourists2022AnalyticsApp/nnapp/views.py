from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Subquery, OuterRef
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
import json
import requests
import folium
from folium.plugins import HeatMap
import numpy as np

# Create your views here.
#Thank you, prewritten comment in Django

def mainpage(request):
    # data = [
    #     ['Year', 'Sales', 'Expenses'],
    #     ['2013', 1000, 400],
    #     ['2014', 1170, 460],
    #     ['2015', 660, 1120],
    #     ['2016', 1030, 540]
    # ]

    count_by_month = requests.get("http://127.0.0.1:2137/count_sort/month").json()
    # Формируем массив для Google Charts
    count_by_month_data = [['Month', 'Tourists']]
    for item in count_by_month:
        count_by_month_data.append([item['name'].replace("2022-", ""), item['count']])

    count_by_gender = requests.get("http://127.0.0.1:2137/count_sort/gender").json()
    # Формируем массив для Google Charts
    count_by_gender_data = [['Gender', 'Tourists']]
    for item in count_by_gender:
        count_by_gender_data.append([item['name'], item['count']])

    count_by_tourist_age = requests.get("http://127.0.0.1:2137/count_sort/tourist_age").json()
    # Формируем массив для Google Charts
    count_by_tourist_age_data = [['Tourist age', 'Tourists']]
    for item in count_by_tourist_age:
        count_by_tourist_age_data.append([item['name'], item['count']])

    rows = requests.get("http://127.0.0.1:2137/count_sort_geo/home_country").json()
    # Данные для тепловой карты: [[lat, lng, weight], ...]
    heat_data = []
    for row in rows:
        heat_data.append([float(row["latitude"]), float(row["longitude"]), int(row["count"]), str(row["name"])])
    # Создаём карту
    map_obj = folium.Map(
        location=[0.0,0.0],
        zoom_start=1,
        tiles='OpenStreetMap'
    )
    # Добавляем маркеры для районов с большим количеством поездок
    for item in heat_data:
        folium.CircleMarker(
            location=[item[0], item[1]],
            radius=max(2, item[2] ** 0.3),
            popup=f"{item[3]} {item[2]}",
            color='red',
            fill=True
        ).add_to(map_obj)
    # Сохраняем карту в строку
    map_html = map_obj._repr_html_()

    rows = requests.get("http://127.0.0.1:2137/count_sort_geo/home_region").json()
    # Данные для тепловой карты: [[lat, lng, weight], ...]
    heat_data_reg = []
    for row in rows:
        if row["name"]!="Не указан":
            heat_data_reg.append([float(row["latitude"]), float(row["longitude"]), int(row["count"]), str(row["name"])])
    # Создаём карту
    map_obj_reg = folium.Map(
        location=[61.79, 96.35],
        zoom_start=2,
        tiles='OpenStreetMap'
    )
    # Добавляем маркеры для районов с большим количеством поездок
    for item in heat_data_reg:
        folium.CircleMarker(
            location=[item[0], item[1]],
            radius=max(2, item[2] ** 0.3),
            popup=f"{item[3]} {item[2]}",
            color='red',
            fill=True
        ).add_to(map_obj_reg)
    # Сохраняем карту в строку
    map_html_reg = map_obj_reg._repr_html_()

    rows = requests.get("http://127.0.0.1:2137/count_sort_geo/home_city").json()
    # Данные для тепловой карты: [[lat, lng, weight], ...]
    heat_data_city = []
    for row in rows:
        if row["name"] != "Не указан":
            heat_data_city.append([float(row["latitude"]), float(row["longitude"]), int(row["count"]), str(row["name"])])
    # Создаём карту
    map_obj_city = folium.Map(
        location=[56.32, 44.53],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    # Добавляем маркеры для районов с большим количеством поездок
    for item in heat_data_city:
        folium.CircleMarker(
            location=[item[0], item[1]],
            radius=max(2, item[2] ** 0.3),
            popup=f"{item[3]} {item[2]}",
            color='red',
            fill=True
        ).add_to(map_obj_city)
    # Сохраняем карту в строку
    map_html_city = map_obj_city._repr_html_()

    avg_values = requests.get("http://127.0.0.1:2137/avg_values").json()

    average_by_month = requests.get("http://127.0.0.1:2137/count_sort/month").json()
    # Формируем массив для Google Charts
    average_by_month_data = [['Month', 'Average Value']]
    for item in average_by_month:
        average_by_month_data.append([item['name'], item['average']])

    rows = requests.get("http://127.0.0.1:2137/cohort_geo/home_region").json()
    # Данные для тепловой карты: [[lat, lng, weight], ...]
    heat_data_reg_spent = []
    for row in rows:
        if row["name"] != "Не указан":
            heat_data_reg_spent.append([float(row["latitude"]), float(row["longitude"]), float(row["avg_spent"]), str(row["name"])])
    # Создаём карту
    map_obj_reg_spent = folium.Map(
        location=[61.79, 96.35],
        zoom_start=2,
        tiles='OpenStreetMap'
    )
    # Добавляем маркеры для районов с большим количеством поездок
    for item in heat_data_reg_spent:
        folium.CircleMarker(
            location=[item[0], item[1]],
            radius=max(2, item[2]*100),
            popup=f"{item[3]} {item[2]}",
            color='red',
            fill=True
        ).add_to(map_obj_reg_spent)
    # Сохраняем карту в строку
    map_html_reg_spent = map_obj_reg_spent._repr_html_()

    return render(request, 'mainpage.html', {
        'count_by_month': json.dumps(count_by_month_data),
        'count_tourists': sum([i["count"] for i in count_by_month]),
        'count_by_gender': json.dumps(count_by_gender_data),
        'count_by_tourist_age': json.dumps(count_by_tourist_age_data),
        'map_html': map_html,
        'map_html_reg': map_html_reg,
        'map_html_city': map_html_city,
        'avg_spent': avg_values[0]["avg_spent"]*1000000,
        'average_by_month': json.dumps(average_by_month_data),
        'map_html_reg_spent': map_html_reg_spent
    })
