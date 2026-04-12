"""
main.py — CLI entry point for LowBid.

Run:  python main.py
"""
import os # used to handle file paths

from bst import Bid_tree # import the binary search tree class
from loader import load_bid # import function to load bids from file
from simulation import run_simulation # import simulation function


if __name__ == "__main__": # check if this file is executed directly
    data_file = os.path.join('data', 'lowbid_manche_demo.csv') # build file path
    bids = load_bid(data_file) # load bids from CSV file

    if bids: # check if there are bids
        tree = Bid_tree() # create a new tree
        tree.build_tree(bids) # insert all bids into the tree

        print("=== In-order traversal ===")
        for node in tree.get_inorder_nodes(): # loop through sorted nodes
            status = "UNIQUE" if len(node.names) == 1 else "DUPLICATE" # check if bid is unique
            print(f"  {node.bid}: {node.names} -> {status}") # display bid info

        print(f"\nTree depth    : {tree.depth()} {'(DEGENERATE)' if tree.is_degenerate() else ''}") # show tree depth and check if it is unbalanced

        winner = tree.find_winner() # find lowest unique bid
        if winner:
            print(f"Winner        : {winner.names[0]} with price {winner.bid}") # show winner
        else:
            print("No winner this round.") # no unique bid

        print(f"\nTotal bids    : {tree.total_bids()}") # total number of bids
        print(f"Seller revenue: ${tree.seller_revenue():.2f}") # total money earned
        print(f"Avg cost/bid  : ${tree.average_cost_per_player():.2f}") # average cost per player

    print("\n=== Simulation (500 rounds) ===")
    results = run_simulation(num_rounds=500, num_players=20, max_price=50) # run simulation with many rounds
    for strategy, r in results.items(): # loop through each strategy
        print(f"\n[{strategy}]")
        print(f"  Win rate          : {r['win_rate']:.1%}") # percentage of wins
        print(f"  Avg winning price : {r['avg_winning_price']:.2f}") # average winning bid
        print(f"  Avg seller revenue: ${r['avg_seller_revenue']:.2f}") # average revenue
