""" update_db_file.py: pull from the database and write an anonymized json file suitable for publishing.
Requires secrets file. Published only for posterity; you won't be able to run this.

author: Spencatro
"""

import json
import os
import pymongo
from dateutil.parser import parse as parse_date

prod_debug_password = None
prod_mongo_url = None

if os.path.exists("secrets"):
    with open("secrets", "r") as rf:
        for line in rf.readlines():
            key, value = line.strip().split("=")
            if key == "MONGO_URL":
                prod_mongo_url = value

mongo_url = prod_mongo_url
mongo_client = pymongo.MongoClient(mongo_url)

game = mongo_client["mtgatracker"]["game"]
singleton_query = {
    "date": {
        "$gt": parse_date("2018-08-01T15:28:59.048Z"),
        "$lt": parse_date("2018-08-27T15:28:59.048Z")
    },
    "eventID": {"$exists": True}
}
quickexplore_query = {
    "date": {
        "$gt": parse_date("2018-08-23T06:28:59.048Z"),
        "$lt": parse_date("2018-08-28T15:28:59.048Z")
    },
    "eventID": {"$exists": True}
}
query = quickexplore_query
print(game.find(query).count())

anon_user_lookup = {}

anon_games = []

for game in game.find(query):
    if game["hero"] not in anon_user_lookup:
        anon_user_lookup[game["hero"]] = "player{}".format(len(anon_user_lookup.keys()))
    anon_games.append({
        "eventID": game["eventID"],
        "won": game["winner"] == game["hero"],
        "player": anon_user_lookup[game["hero"]]
    })

with open("games.json", "w") as wp:
    json.dump({"games": anon_games}, wp)