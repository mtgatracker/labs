"""  event_split_analysis.py: perform analysis on how frequently each event is played

"""
import json

from collections import defaultdict

with open("singleton_games.json", "r") as rp:
    all_games = json.load(rp)["games"]

# for the first graph, we want to strictly limit between when the first explore game occurred and the last. The query
# that built games.json is pretty close with some buffer on each end to show context, but we can be exact in code
# here, and that's what we want to do

first_idx = len(all_games)
last_idx = 0

for idx, game in enumerate(all_games):
    if game["eventID"] == "QuickExploration_08242018":
        first_idx = min(idx, first_idx)
        last_idx = max(idx, last_idx)

print(len(all_games))
print(first_idx)
print(last_idx)
print(all_games[first_idx])
print(all_games[last_idx])

strict_event_id_counts = defaultdict(int)
for game in all_games[first_idx:last_idx]:
    strict_event_id_counts[game["eventID"]] += 1

strict_event_infos = []
for key in strict_event_id_counts.keys():
    strict_event_infos.append({"name": key, "count": strict_event_id_counts[key]})
strict_event_infos.sort(key=lambda x: x["count"], reverse=True)

print([event["name"] for event in strict_event_infos])
print([event["count"] for event in strict_event_infos])

event_id_counts = defaultdict(int)
for game in all_games:
    event_id_counts[game["eventID"]] += 1

event_infos = []
for event in event_id_counts.keys():
    event_infos.append({"name": event, "count": event_id_counts[event], "percent": 100.0 * event_id_counts[event] / float(len(all_games)), "step_percents": []})

event_infos.sort(key=lambda x: x["count"], reverse=True)

names = [event["name"] for event in event_infos]
pcts = [event["count"] for event in event_infos]

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

num_ticks = 70
range_per_tick = len(all_games) / num_ticks
for tick in range(1, num_ticks - 10):
    event_id_count_steps = defaultdict(int)
    start_idx = max(0, int(tick * range_per_tick))
    end_idx = min(len(all_games), int((tick + 18) * range_per_tick))
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