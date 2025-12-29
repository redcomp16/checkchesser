from .player import Player
from .uscf_service import USCF_Service
import csv

def Load_Players(csv_path = "players/players.csv"):
    players = {}

    with open(csv_path, newline = "") as file:
        reader = csv.DictReader(file, skipinitialspace = True)

        for row in reader:
            first_name = row["first_name"]
            last_name = row["last_name"]
            name = f"{first_name} {last_name}"
            school = row["school"]
            grade = row["grade"]
            uscf_id = row["uscf_id"]
            players[name] = Player(name, school, grade, uscf_id)
        
        return players
