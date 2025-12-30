import requests
from player import Player
import time

class USCF_Service:

    session = requests.Session()
    last_request_time = 0
    min_interval = 0.5

    @classmethod
    def get(cls, url):
        elapsed = time.time() - cls._last_request_time
        if elapsed < cls.min_interval:
            time.sleep(cls.min_interval - elapsed)

        response = cls.session.get(url, timeout=10)
        cls._last_request_time = time.time()
        response.raise_for_status()
        return response.json()

    @classmethod
    def update_official_rating(cls, player: Player):
        data = cls.get(player.main_link).json()
        official_rating = data["ratings"][0]["rating"]
        player.official_rating = official_rating
    
    @classmethod
    def update_live_rating(cls, player: Player):
        time.sleep(0.5)
        data = cls.get(player.history_link).json()
        ratings = [r for section in data["items"] for r in section["ratingRecords"]]
        most_recent = sorted(ratings, key = lambda r: r.get("event", {}).get("date", ""), reverse = True)[0]
        live_rating = most_recent["postRating"]
        try:
            pre_rating = most_recent["preRating"]
        except KeyError:
            pre_rating = 0
        delta_live_rating = live_rating - pre_rating
        player.live_rating = live_rating
        player.delta_live_rating = delta_live_rating

    @classmethod
    def update_ratings(cls, player: Player):
        cls.update_official_rating(player)
        cls.update_live_rating(player)
