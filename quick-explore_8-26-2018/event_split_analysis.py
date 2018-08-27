"""  event_split_analysis.py: perform analysis on how frequently each event is played

"""
import json

from collections import defaultdict

with open("games.json", "r") as rp:
    all_games = json.load(rp)["games"]

event_id_counts = defaultdict(int)
for game in all_games:
    event_id_counts[game["eventID"]] += 1

event_infos = []
for event in event_id_counts.keys():
    event_infos.append({"name": event, "count": event_id_counts[event], "percent": 100.0 * event_id_counts[event] / float(len(all_games)), "step_percents": []})

event_infos.sort(key=lambda x: x["count"], reverse=True)

names = [event["name"] for event in event_infos]
pcts = [event["count"] for event in event_infos]

print("event pcts")
print(names)
print(pcts)

# method one: calculate percents by each step remembering entire history (the first game counts on the last tick)
# note: tracking every single step after every single game would yield WAY too many data points
# so we need to somehow define steps, then take the average within those steps
#
# event_id_count_steps = defaultdict(int)
# for idx, game in enumerate(all_games):
#     event_id_count_steps[game["eventID"]] += 1
#     for event_info in event_infos:
#         name = event_info["name"]
#         event_pct_step = 100 * event_id_count_steps[name] / float(idx + 1)
#         if idx % 100 == 5:
#             event_info["step_percents"].append(event_pct_step)


# method two: calculate percents by each step with limited lookback history
#   (the first game DOES NOT count on the last tick)

num_ticks = 10
range_per_tick = len(all_games) / num_ticks
for tick in range(1, num_ticks):
    event_id_count_steps = defaultdict(int)
    start_idx = max(0, int((tick - 1) * range_per_tick))
    end_idx = min(len(all_games), int((tick + 2) * range_per_tick))
    for idx in range(start_idx, end_idx):
        game = all_games[idx]
        event_id_count_steps[game["eventID"]] += 1
    for event_info in event_infos:
        name = event_info["name"]
        event_pct_step = 100 * event_id_count_steps[name] / (end_idx - start_idx)
        event_info["step_percents"].append(event_pct_step)

data_set_template = """
        {{
          label: '{}',
          data: {},
          borderColor: niceColors[{}],
          backgroundColor: "rgba(0, 0, 0, 0)",
          borderWidth: 2,
          pointRadius: 1,
          lineTension: 0.2,
        }},
"""

data_template = """
let lineData = {{
  datasets: [{}],
  labels: [{}]
}}
"""

datasets = []
for idx, event in enumerate(event_infos):
    datasets.append(data_set_template.format(event["name"], event["step_percents"], idx))

print(data_template.format("".join(datasets).strip(), "'',"*len(event_infos[0]["step_percents"])))