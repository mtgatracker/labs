# Convert MTGA Collection to MTGGoldfish

Requested by a user in our discord. To use:

- Find `GetPlayerCardsV3` in output_log.txt
- Save the blob as `mtga_collection.json`
- `python convert_to_mtgg.py -i mtga_collection.json -o mtgg_collection.csv`