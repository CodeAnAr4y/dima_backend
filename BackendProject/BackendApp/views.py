from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def index(request):
    return render(request, 'backendapp/index.html')

def login_view(request):
    return JsonResponse({"name": "Arthur", "surename": "Sultanov"}, status=200)