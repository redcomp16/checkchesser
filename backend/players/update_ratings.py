import csv
import sys
import os
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "players.csv"

sys.path.append(str(BASE_DIR.parent))

from .load_players import Load_Players
from .uscf_service import USCF_Service

def update_ratings():
    players = Load_Players()

    for name, player in players.items():
        print(f"Updating {name}...")
        USCF_Service.update_ratings(player)

    fieldnames = ["first_name", "last_name", "school", "grade", "uscf_id", "official_rating", "live_rating", "delta_live_rating"]
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in players.values():
            name_parts = p.name.split(" ", 1)
            writer.writerow({
                "first_name": name_parts[0],
                "last_name": name_parts[1] if len(name_parts) > 1 else "",
                "school": p.school,
                "grade": p.grade,
                "uscf_id": p.uscf_id,
                "official_rating": p.official_rating,
                "live_rating": p.live_rating,
                "delta_live_rating": getattr(p, 'delta_live_rating', 0)
            })

if __name__ == "__main__":
    update_ratings()
