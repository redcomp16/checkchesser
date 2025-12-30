from rest_framework.decorators import api_view
from rest_framework.response import Response

from .load_players import Load_Players
from .filter_players import Filter_Players

GetPlayers = Load_Players()

@api_view(["GET"])
def players(request):

    players = GetPlayers

    name = request.GET.get("name")
    min_rating = request.GET.get("min_rating")
    max_rating = request.GET.get("max_rating")
    school = request.GET.get("school")
    grade = request.GET.get("grade")

    min_rating = int(min_rating) if min_rating is not None else None
    max_rating = int(max_rating) if max_rating is not None else None

    f_players = Filter_Players(
        players,
        name=name,
        min_rating=min_rating,
        max_rating=max_rating,
        school=school,
        grade=grade
    )
    
    data = [
        {
            "name": p.name,
            "school": p.school,
            "grade": p.grade,
            "uscf_id": p.uscf_id,
            "official_rating": p.official_rating,
            "live_rating": p.live_rating,
            "delta_live_rating": p.delta_live_rating,
        }
        for p in f_players
    ]

    return Response(data)