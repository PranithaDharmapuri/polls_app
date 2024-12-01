from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'Descriptions/home.html')

def details_des(request):
    return render(request,'Descriptions/details_des.html')