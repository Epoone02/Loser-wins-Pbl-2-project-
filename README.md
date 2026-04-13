# Loser-wins-Pbl-2-project-Winabid

A reverse-auction platform where the **lowest unique bid wins**.  
The winner is not who bids the most, but who picks the smallest price that **no one else chose**.

---

## Project structure

```
lowbid/
├── streamlit_app.py        # Homepage & navigation
├── main.py                 # CLI entry point (demo + simulation)
├── bst.py                  # BidNode + Bid_tree (all BST logic)
├── simulation.py           # simulate_round, run_simulation
├── utils.py                # load_bid, compute_bid_cost
│
├── pages/
│   ├── PlayerVSPlayer.py   # Live game UI (player & host views)
│   └── Chart.py            # Stats, charts & strategy simulation
│
└── data/
    ├── lowbid_manche_demo.csv          # 30 bids — quick demo
    ├── lowbid_multi_manches_500x40.csv # 500 rounds × 40 players
    └── lowbid_stress_200k.csv          # 200 000 bids — stress test
```

---

## Installation

Our code interface works with Streamlit, so you may need to install it if you haven't already.

```bash
pip install streamlit pandas altair
```
if needed here is the upgrade command for Streamlit

```bash
pip install --upgrade streamlit
```

---

## Running the app

**Always launch from the project root folder:**

```bash
# Windows
py -m streamlit run streamlit_app.py

# Mac / Linux
streamlit run streamlit_app.py
```

> /!\ Do **not** run from inside the `pages/` folder — the `data/` files won't be found.

---

##  Running the CLI

```bash
python main.py
```

Loads the demo CSV, prints the in-order traversal, finds the winner, and runs a 500-round simulation.

---

## How the game works

1. Every player places a bid (integer ≥ 0).
2. The **winner** is the player with the **lowest price that no one else chose**.
3. Every bid costs money — the lower the price, the higher the cost:

```
cost(price) = base_cost + α / (price + 1)
```

4. If no price is unique, the round has **no winner**.

---

## Data structure — Binary Search Tree (BST)

Bids are stored in a BST keyed by price. Each node holds a **list of players** who placed that price, so duplicates are handled natively without extra data structures.

| Operation | Average | Worst case |
|---|---|---|
| `insert` | O(log n) | O(n) — degenerate tree |
| `search` | O(log n) | O(n) |
| `successor` / `predecessor` | O(log n) | O(n) |
| `delete` | O(log n) | O(n) |
| `find_winner` (in-order scan) | O(n) | O(n) |

> **Degeneration:** inserting bids in sorted order turns the BST into a linked list (depth = n). Use `tree.depth()` and `tree.is_degenerate()` to detect this.

---

## Simulation strategies

| Strategy | Distribution | Behaviour |
|---|---|---|
| `random` | Uniform `[0, max_price]` | Baseline — no strategy |
| `low_bias` | Exponential (skewed toward 0) | Aggressive low bids — high cost |
| `mid_range` | Normal (centered at `max_price / 2`) | Avoids extremes — lower cost |

---

## CSV formats supported

| Format | Columns | Example |
|---|---|---|
| Single round | `joueur, prix` | `J01, 5` |
| Multi-round | `manche, joueur, prix` | `1, J01, 42` |

Both formats are detected automatically by `load_bid()`.

---

## Authors

Raffael Raffiani - Emilio Patino - Alexandre Stepien - Alexandre Amon - Gabriel Assouline