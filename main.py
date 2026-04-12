"""
main.py — CLI entry point for LowBid.

Run:  python main.py
"""
import os

from bst import Bid_tree
from loader import load_bid
from simulation import run_simulation


if __name__ == "__main__":
    data_file = os.path.join('data', 'lowbid_manche_demo.csv')
    bids = load_bid(data_file)

    if bids:
        tree = Bid_tree()
        tree.build_tree(bids)

        print("=== In-order traversal ===")
        for node in tree.get_inorder_nodes():
            status = "UNIQUE" if len(node.names) == 1 else "DUPLICATE"
            print(f"  {node.bid}: {node.names} -> {status}")

        print(f"\nTree depth    : {tree.depth()} {'(DEGENERATE)' if tree.is_degenerate() else ''}")

        winner = tree.find_winner()
        if winner:
            print(f"Winner        : {winner.names[0]} with price {winner.bid}")
        else:
            print("No winner this round.")

        print(f"\nTotal bids    : {tree.total_bids()}")
        print(f"Seller revenue: ${tree.seller_revenue():.2f}")
        print(f"Avg cost/bid  : ${tree.average_cost_per_player():.2f}")

    print("\n=== Simulation (500 rounds) ===")
    results = run_simulation(num_rounds=500, num_players=20, max_price=50)
    for strategy, r in results.items():
        print(f"\n[{strategy}]")
        print(f"  Win rate          : {r['win_rate']:.1%}")
        print(f"  Avg winning price : {r['avg_winning_price']:.2f}")
        print(f"  Avg seller revenue: ${r['avg_seller_revenue']:.2f}")
