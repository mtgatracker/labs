import argparse
import json
import mtga
import csv

header = ["Card", "Set ID", "Set Name", "Quantity", "Foil"]


def read_collection(input_filename):
    with open(input_filename, 'r') as input_file:
        collection = json.load(input_file)
    return collection


def write_collection(collection, output_filename):
    rows = []
    for card_key in collection.keys():
        count = collection[card_key]
        try:
            card = mtga.all_mtga_cards.find_one(card_key)
            assert isinstance(card, mtga.card.Card)
            rows.append((card.pretty_name, card.set, "", count, 0))
        except Exception:  # firesong and sunspeaker
            print("couldn't find card: {}".format(card_key))
    with open(output_filename, 'w', newline='') as out_file:
        output_writer = csv.writer(out_file)
        output_writer.writerow(header)
        output_writer.writerows(rows)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default="mtga_collection.json", help="json file to use as input")
    parser.add_argument('-o', '--output', default="mtgg_collection.csv", help="csv file to output")
    args = parser.parse_args()

    collection = read_collection(args.input)
    write_collection(collection, args.output)
