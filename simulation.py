import random

from bst import Bid_tree
from loader import compute_bid_cost


def simulate_round(num_players, max_price, strategy, base_cost=1.0, alpha=49.0):

    tree = Bid_tree()
    total_revenue = 0.0

    for i in range(num_players):
        if strategy == 'random':
            price = random.randint(0, max_price)

        elif strategy == 'low_bias':
            price = min(int(random.expovariate(1 / (max_price * 0.15))), max_price)

        elif strategy == 'mid_range':
            mean = max_price // 2
            price = max(0, min(max_price, int(random.gauss(mean, max_price * 0.15))))

        else:
            raise ValueError(f"Unknown strategy: '{strategy}'")

        tree.insert(f"P{i}", price)
        total_revenue += compute_bid_cost(price, base_cost, alpha)

    winner = tree.find_winner()
    if winner:
        return winner.names[0], winner.bid, total_revenue
    return None, None, total_revenue


def run_simulation(num_rounds=500, num_players=20, max_price=50, base_cost=1.0, alpha=49.0):

    strategies = ['random', 'low_bias', 'mid_range']
    stats = {
        s: {'wins': 0, 'total_price': 0, 'total_revenue': 0.0, 'rounds_with_winner': 0}
        for s in strategies
    }

    for _ in range(num_rounds):
        for strategy in strategies:
            winner_name, winner_price, revenue = simulate_round(
                num_players, max_price, strategy, base_cost, alpha
            )
            stats[strategy]['total_revenue'] += revenue
            if winner_name is not None:
                stats[strategy]['wins'] += 1
                stats[strategy]['total_price'] += winner_price
                stats[strategy]['rounds_with_winner'] += 1

    results = {}
    for s in strategies:
        won = stats[s]['rounds_with_winner']
        results[s] = {
            'win_rate':           stats[s]['wins'] / num_rounds,
            'avg_winning_price':  stats[s]['total_price'] / won if won > 0 else 0,
            'avg_seller_revenue': stats[s]['total_revenue'] / num_rounds,
            'rounds_with_winner': won,
        }
    return results
