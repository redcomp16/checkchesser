from django.urls import path
from .leaderboard import players

urlpatterns = [
    path("players/", players),
]