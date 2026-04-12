import streamlit as st
import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bst import Bid_tree
from loader import compute_bid_cost

@st.cache_resource
def get_global_memory():
    return {
        "bids": [],
        "bank": {},
        "base_cost": 1.0,
        "alpha": 49.0,
        "max_price": 99,
        "num_bots": 10,
    }

def get_wins():
    return []

memory = get_global_memory()
wins = get_wins()

st.sidebar.title("⚙️ Game Settings")
current_view = st.sidebar.radio("Switch View:", ["👤 Player View", "🎛️ Host View"])


if current_view == "👤 Player View":
    st.title("Place Your Bid!")

    base_cost  = memory['base_cost']
    alpha      = memory['alpha']
    max_price  = memory['max_price']

    player_name = st.text_input("Enter your Username:")

    if player_name:
        if player_name not in memory["bank"]:
            memory['bank'][player_name] = 100.0

        current_balance = memory['bank'][player_name]
        st.info(f"**Current Balance:** ${current_balance:.2f}")

        if current_balance > 0:
            max_bid = min(int(current_balance), max_price)
            proposed_price = st.slider(
                "Select your Bid Price",
                min_value=0, max_value=max(max_bid, 1), value=0, step=1
            )

            bid_cost = compute_bid_cost(proposed_price, base_cost, alpha)
            st.write(f"**Cost of this ticket:** ${bid_cost:.2f}")

            # Show successor/predecessor hint
            existing_tree = Bid_tree()
            for b in memory['bids']:
                existing_tree.insert(b['name'], b['price'])

            succ = existing_tree.successor(proposed_price)
            pred = existing_tree.predecessor(proposed_price)
            if succ or pred:
                hints = []
                if pred:
                    hints.append(f"Closest lower bid already placed: **{pred.bid}**")
                if succ:
                    hints.append(f"Closest higher bid already placed: **{succ.bid}**")
                st.caption(" | ".join(hints))

            if bid_cost > current_balance:
                st.error("You don't have enough money to pay the ticket cost!")
            else:
                if st.button("Submit Bid"):
                    memory['bank'][player_name] -= bid_cost
                    memory['bids'].append({
                        "name": player_name,
                        "price": proposed_price,
                        "cost": bid_cost
                    })
                    st.success(f"Bid of **{proposed_price}** placed! Remaining balance: ${memory['bank'][player_name]:.2f}")
        else:
            st.error("You are bankrupt!")


elif current_view == "🎛️ Host View":
    st.title("Host Dashboard 🎛️")

    with st.expander("⚙️ Configure Game Rules", expanded=False):
        memory['base_cost']  = st.number_input("Base Cost",          min_value=0.0,  value=memory['base_cost'],  step=0.5)
        memory['alpha']      = st.number_input("Alpha Parameter (α)", min_value=0.0, value=memory['alpha'],      step=1.0)
        memory['max_price']  = st.number_input("Max Bid Price",       min_value=1,   value=memory['max_price'],  step=1)
        memory['num_bots']   = st.number_input("Number of Bot Players", min_value=0, value=memory['num_bots'],   step=1)

    st.write(f"**Total bids received:** {len(memory['bids'])}")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Add Bot Bids", help="Bots play with random strategy"):
            base_cost = memory['base_cost']
            alpha     = memory['alpha']
            max_price = memory['max_price']
            num_bots  = int(memory['num_bots'])

            strategies = ['random', 'low_bias', 'mid_range']
            for i in range(num_bots):
                strategy = random.choice(strategies)
                if strategy == 'random':
                    price = random.randint(0, max_price)
                elif strategy == 'low_bias':
                    price = min(int(random.expovariate(1 / (max_price * 0.15))), max_price)
                else:
                    mean  = max_price // 2
                    price = max(0, min(max_price, int(random.gauss(mean, max_price * 0.15))))

                cost      = compute_bid_cost(price, base_cost, alpha)
                bot_name  = f"Bot_{strategy[:3].upper()}_{i}"
                memory['bids'].append({"name": bot_name, "price": price, "cost": cost})

            st.success(f"Added {num_bots} bot bids!")
            st.rerun()

    with col2:
        if st.button("Clear All Bids"):
            memory['bids'] = []
            st.rerun()

    st.divider()

    if len(memory['bids']) > 0:
        if st.button("Resolve Round", type="primary"):
            tree              = Bid_tree()
            total_seller_rev  = 0.0

            for bid in memory['bids']:
                tree.insert(bid["name"], bid["price"])
                total_seller_rev += bid["cost"]

            sorted_nodes = tree.get_inorder_nodes()
            winner       = tree.find_winner()

            st.subheader("Bid Results (Ascending Order)")
            for node in sorted_nodes:
                num_players = len(node.names)
                status      = "UNIQUE" if num_players == 1 else "DUPLICATE"
                st.write(f"- Price **{node.bid}** — {num_players} player(s) ({', '.join(node.names)}) → {status}")

                # Show successor for non-unique bids (next candidate to check)
                if num_players > 1:
                    succ = tree.successor(node.bid)
                    if succ:
                        st.caption(f"  ↳ Next candidate price (successor): **{succ.bid}**")

            st.divider()
            st.subheader("Final Result")

            if winner:
                wins.append(node.bid)
                st.balloons()
                st.success(f"The winner is **{winner.names[0]}** with the unique price of **{winner.bid}**!")
            else:
                st.warning("No winner! Every price was proposed at least twice.")

            st.metric(label="Seller Revenue", value=f"${total_seller_rev:.2f}")
    else:
        st.info("Waiting for players to place bids…")
