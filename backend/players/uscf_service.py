import requests
import time
from .player import Player

class USCF_Service:

    @staticmethod
    def _safe_get(url, max_retries=3):

        delay = 1.0 
        for attempt in range(max_retries):
            time.sleep(delay)
            
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                
                if response.status_code == 429:
                    wait_time = int(response.headers.get("Retry-After", 2 ** (attempt + 1)))
                    print(f"Rate limited (429). Waiting {wait_time}s before retry {attempt + 1}...")
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                
            except (requests.RequestException, ValueError) as e:
                if attempt == max_retries - 1:
                    print(f"Request failed after {max_retries} attempts: {e}")
                    return None
                continue
        return None

    @staticmethod
    def update_official_rating(player: Player):
        data = USCF_Service._safe_get(player.main_link)
        if data:
            try:
                official_rating = data.get("ratings", [{}])[0].get("rating", 0)
                player.official_rating = official_rating
            except (IndexError, KeyError):
                player.official_rating = 0
        else:
            print(f"Failed to fetch official rating for {player.name}")
            player.official_rating = 0

    @staticmethod
    def update_live_rating(player: Player):
        data = USCF_Service._safe_get(player.history_link)
        if not data:
            print(f"Failed to fetch live rating for {player.name}")
            player.live_rating = 0
            return

        try:
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
                
        except (IndexError, KeyError, ValueError) as e:
            print(f"Error parsing live rating for {player.name}: {e}")
            player.live_rating = 0

    @staticmethod
    def update_ratings(player: Player):
        USCF_Service.update_official_rating(player)
        USCF_Service.update_live_rating(player)
