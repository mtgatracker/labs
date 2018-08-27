"""  count_user_entries.py: perform analysis on how many times each player enters QE

"""
import json
from collections import defaultdict

with open("games.json", "r") as rp:
    all_games = json.load(rp)["games"]

quick_explore_game_results = defaultdict(list)
player_entries = dict()

for game in all_games:
    if game["eventID"] == "QuickExploration_08242018":
        quick_explore_game_results[game["player"]].append(game["won"])

# count total unique players
print(len(set([p["player"] for p in all_games])))
# count unique players who played QE
print(len(quick_explore_game_results.keys()))

for player in quick_explore_game_results.keys():
    player_record = quick_explore_game_results[player]
    last_record = []
    entries = 1
    for game in player_record:
        # need to iterate across all player's games and split them into event entries
        if (len(last_record)) > 2:
            # if they have 2+ games already, they must have either two wins or two losses; it's over
            entries += 1
            last_record = []
        if len(last_record) > 1:
            # if they have 1+, we need to check if it is WW or LL
            if last_record[0] == last_record[1]:
                last_record = []
                entries += 1
        last_record.append(game)
    player_entries[player] = entries

# sort players into buckets based on how many times they played QE
buckets = defaultdict(int)
for player in player_entries:
    buckets[player_entries[player]] += 1

max_key = max(buckets.keys())
keys = range(1, max_key + 1)

print(list(keys))
print([buckets[k] for k in keys])