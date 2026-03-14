import requests
from .player import Player
import time

class USCF_Service:

    @staticmethod
    def update_official_rating(player: Player):
        time.sleep(1.0)
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
        time.sleep(1.0)
        try:
            response = requests.get(player.history_link, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            all_records = []
            for item in data.get("items", []):
                event_date = item.get("event", {}).get("endDate", "")
                for record in item.get("ratingRecords", []):
                    record["_date"] = event_date
                    all_records.append(record)
    
            regular_records = [r for r in all_records if r.get("ratingSource") == "R"]
    
            if regular_records:
                most_recent = sorted(
                    regular_records, 
                    key=lambda r: r.get("_date", ""), 
                    reverse=True
                )[0]
                
                live_rating = most_recent.get("postRating", 0)
                pre_rating = most_recent.get("preRating", 0)
                
                player.live_rating = live_rating
                player.delta_live_rating = live_rating - pre_rating
            else:
                player.live_rating = player.official_rating if player.official_rating else 0
                player.delta_live_rating = 0
                
        except (requests.RequestException, ValueError, IndexError, KeyError) as e:
            print(f"Failed to fetch live rating for {player.name}: {e}")
            player.live_rating = 0

    @staticmethod
    def update_ratings(player: Player):
        USCF_Service.update_official_rating(player)
        USCF_Service.update_live_rating(player)
