# quick-explore_8-26-2018

Source code used to retrieve, arrange, and analyze data for
[Report: Exploring Weekend Events](https://blog.mtgatracker.com/report-exploring-weekend-events)
(plus a fruitless sim experiment)

## To use:

1. `python update_db_file.py` to generate games.json (note: won't work unless you have `secrets` (you don't))
1. `python event_split_analysis.py` to generate `lineData` for the blog post
1. `python count_quick_explore_entries.py` to generate info for donut graphs