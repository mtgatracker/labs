"""  count_user_entries.py: perform analysis on how many times each player enters QS

"""
import json
from collections import defaultdict

with open("singleton_games.json", "r") as rp:
    all_games = json.load(rp)["games"]

quick_singleton_game_results = defaultdict(list)
player_entries = dict()

for game in all_games:
    if game["eventID"] == "Quick_Singleton_08092018":
        quick_singleton_game_results[game["player"]].append(game["won"])

# count total unique players
print(len(set([p["player"] for p in all_games])))
# count unique players who played QS
print(len(quick_singleton_game_results.keys()))

for player in quick_singleton_game_results.keys():
    player_record = quick_singleton_game_results[player]
    last_record = []
    entries = 1
    for game in player_record:
        # need to iterate across all player's games and split them into event entries
        if last_record.count(True) > 2 or last_record.count(False) > 6:
            # 3 losses or 7 wins is the cutoff
            entries += 1
            last_record = []
        last_record.append(game)
    player_entries[player] = entries

# sort players into buckets based on how many times they played QS
buckets = defaultdict(int)
for player in player_entries:
    buckets[player_entries[player]] += 1

max_key = max(buckets.keys())
keys = range(1, max_key + 1)

print(list(keys))
print([buckets[k] for k in keys])
