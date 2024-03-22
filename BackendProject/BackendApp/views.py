from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Works")

def login_view(request):
    return JsonResponse({"name": "Arthur", "surename": "Sultanov"}, status=200)