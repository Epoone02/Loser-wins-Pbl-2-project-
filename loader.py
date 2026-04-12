import csv
import os


def load_bid(file):
    bid_list = []
    if not os.path.exists(file):
        print(f"[WARNING] File not found: {file}")
        return bid_list
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)
        if header is None:
            return bid_list

        # Detect column layout from header names
        header_lower = [h.strip().lower() for h in header]
        if 'manche' in header_lower:
            # 3-column format: manche, joueur, prix
            idx_player = header_lower.index('joueur')
            idx_price  = header_lower.index('prix')
        else:
            # 2-column format: joueur, prix (fallback: col 0 and 1)
            idx_player = 0
            idx_price  = 1

        for row in reader:
            if len(row) > max(idx_player, idx_price):
                try:
                    int(row[idx_price])
                    bid_list.append((row[idx_player], row[idx_price]))
                except ValueError:
                    pass
    return bid_list


def compute_bid_cost(price, base_cost=1.0, alpha=49.0):
    return base_cost + alpha / (price + 1)
