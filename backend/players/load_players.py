from .player import Player
from .uscf_service import USCF_Service

import csv
import os
from pathlib import Path

PARENT_DIR = Path(__file__).resolve().parent

def Load_Players(csv_path=None):
    if csv_path is None:
        csv_path = PARENT_DIR / "players.csv"
        
    players = {}

    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        for row in reader:
            first_name = row["first_name"]
            last_name = row["last_name"]
            name = f"{first_name} {last_name}"
            school = row["school"]
            grade = row["grade"]
            uscf_id = row["uscf_id"]
            official_rating = int(row["official_rating"])
            live_rating = int(row["live_rating"])
            delta_live_rating = int(row["delta_live_rating"])

            players[name] = Player(name, school, grade, uscf_id, official_rating, live_rating, delta_live_rating)
            
    return players
