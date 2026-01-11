import requests
from .player import Player
import time

class USCF_Service:

    @staticmethod
    def update_official_rating(player: Player):
        time.sleep(0.5)
        try:
            response = requests.get(player.main_link, timeout=5)
            response.raise_for_status()  # raise error for non-200 responses
            data = response.json()       # may still raise ValueError if not JSON
            official_rating = data.get("ratings", [{}])[0].get("rating", 0)
            player.official_rating = official_rating
        except (requests.RequestException, ValueError, IndexError, KeyError) as e:
            print(f"Failed to fetch official rating for {player.name}: {e}")
            player.official_rating = 0  # fallback value

    @staticmethod
    def update_live_rating(player: Player):
        time.sleep(0.5)
        try:
            response = requests.get(player.history_link, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            ratings = [
                r for section in data.get("items", []) 
                for r in section.get("ratingRecords", [])
                if r.get("ratingType") == "R"  # This is the crucial line
            ]
            
            if ratings:
                most_recent = sorted(
                    ratings, 
                    key=lambda r: r.get("event", {}).get("date", ""), 
                    reverse=True
                )[0]
                
                live_rating = most_recent.get("postRating", 0)
                pre_rating = most_recent.get("preRating", 0)
                player.live_rating = live_rating
                player.delta_live_rating = live_rating - pre_rating
            else:
                player.live_rating = 0
                player.delta_live_rating = 0
        except (requests.RequestException, ValueError, IndexError, KeyError) as e:
            print(f"Failed to fetch live rating for {player.name}: {e}")
            player.live_rating = 0
            player.delta_live_rating = 0

    @staticmethod
    def update_ratings(player: Player):
        USCF_Service.update_official_rating(player)
        USCF_Service.update_live_rating(player)
