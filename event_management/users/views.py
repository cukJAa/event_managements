from django.shortcuts import render, redirect, HttpResponse
from .models import User



def user_create(request):
    return HttpResponse("Hello, world. You're at the users index.")
