from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests

def index_view(req):
    return render(req, 'main/index.html')