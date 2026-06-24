from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Subquery, OuterRef
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
import json
import requests

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
    # Преобразование в JSON важно для безопасной передачи в JavaScript
    # context = {'data_json': json.dumps(data)}
    url = "http://127.0.0.1:2137/count_sort/month"
    response = requests.get(url)
    context = response.json()
    print(context)
    return render(request, 'mainpage.html', context)

