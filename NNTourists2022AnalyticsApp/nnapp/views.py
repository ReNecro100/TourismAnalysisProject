from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Subquery, OuterRef
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect

# Create your views here.
#Thank you, prewritten comment in Django

def mainpage(request):
    return render(request, 'mainpage.html')