from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

def home(request):
    return render(request, "index.html")

# change func name 
def loginPage(request):
    return render(request, 'login.html') #chng file name 