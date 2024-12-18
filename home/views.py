from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

def home(request):
    return render(request, "index.html")
