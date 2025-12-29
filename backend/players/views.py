from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

def home(request):
    return HttpResponse("<h1>CheckChesser is under construction!</h1>")

@api_view(["GET"])
def players_list(request):
    return Response([
        {
            "name": "Chess Player",
            "school": "Chess HS",
            "grade": 12,
            "uscf_id": "12345678"
        }
    ])
