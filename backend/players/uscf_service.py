import requests
from .player import Player
import time

class USCF_Service:

    @staticmethod
    def update_official_rating(player: Player):
        time.sleep(0.5)
        data = requests.get(player.main_link).json()
        print(player)
        official_rating = data["ratings"][0]["rating"]
        player.official_rating = official_rating
    
    @staticmethod
    def update_live_rating(player: Player):
        time.sleep(1)
        data = requests.get(player.history_link).json()
        ratings = [r for section in data["items"] for r in section["ratingRecords"]]
        most_recent = sorted(ratings, key=lambda r: r.get("event", {}).get("date", ""), reverse=True)[0]
        live_rating = most_recent["postRating"]
        try:
            pre_rating = most_recent["preRating"]
        except KeyError:
            pre_rating = 0
        delta_live_rating = live_rating - pre_rating
        player.live_rating = live_rating
        player.delta_live_rating = delta_live_rating

    @staticmethod
    def update_ratings(player: Player):
        USCF_Service.update_official_rating(player)
        USCF_Service.update_live_rating(player)