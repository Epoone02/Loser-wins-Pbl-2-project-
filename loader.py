import csv
import os


def load_bid(file):
    bid_list = []
    if not os.path.exists(file):
        print(f"[WARNING] File not found: {file}")
        return bid_list
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 2:
                try:
                    int(row[1])
                    bid_list.append((row[0], row[1]))
                except ValueError:
                    pass
    return bid_list


def compute_bid_cost(price, base_cost=1.0, alpha=49.0):
    return base_cost + alpha / (price + 1)
