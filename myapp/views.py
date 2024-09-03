# from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def hello(request):
    return render(request,"index.html")


def vistaLogin(request):
    return render(request,"login.html")