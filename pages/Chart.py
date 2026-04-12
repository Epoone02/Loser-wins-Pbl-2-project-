import streamlit as st
import sys
import os
import pandas as pd
import altair as alt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'APP_lowbid_data')
sys.path.append(BASE_DIR)
from bst import Bid_tree
from simulation import run_simulation
from loader import load_bid, compute_bid_cost

@st.cache_data(show_spinner=False)
def cached_simulation(num_rounds, num_players, max_price, base_cost, alpha):
    return run_simulation(num_rounds, num_players, max_price, base_cost, alpha)

@st.cache_data(show_spinner=False)
def cached_alpha_sweep(num_players, max_price, base_cost):
    """Pre-compute alpha sensitivity across [0..200] — cached so it only runs once per config."""
    rows = []
    STRATEGY_LABELS = {"random": "Random", "low_bias": "Low Bias", "mid_range": "Mid Range"}
    for a in range(0, 201, 10):
        r = run_simulation(100, num_players, max_price, base_cost, float(a))
        for s, stats in r.items():
            rows.append({
                "Alpha": a,
                "Strategy": STRATEGY_LABELS.get(s, s),
                "Avg Seller Revenue": stats["avg_seller_revenue"]
            })
    return pd.DataFrame(rows)

st.title("📊 Stats & Strategy Analysis")


st.sidebar.title("Simulation Settings")
num_rounds  = st.sidebar.slider("Number of rounds",  100, 1000, 500, step=50)
num_players = st.sidebar.slider("Players per round",   5,   50,  20)
max_price   = st.sidebar.slider("Max bid price",      10,  200,  50)
base_cost   = st.sidebar.number_input("Base cost",   value=1.0,  step=0.5)
alpha       = st.sidebar.number_input("Alpha (α)",   value=49.0, step=1.0)

run_btn = st.sidebar.button("▶ Run Simulation", type="primary")

st.subheader("💰 Risk Premium Formula")
st.latex(r"\text{cost}(p) = \text{base\_cost} + \frac{\alpha}{p + 1}")

prices     = list(range(0, max_price + 1))
costs      = [compute_bid_cost(p, base_cost, alpha) for p in prices]
cost_df    = pd.DataFrame({"Price": prices, "Ticket Cost ($)": costs})
cost_chart = alt.Chart(cost_df).mark_line(color="#f97316").encode(
    x=alt.X("Price:Q", title="Bid Price"),
    y=alt.Y("Ticket Cost ($):Q", title="Ticket Cost ($)"),
    tooltip=["Price", "Ticket Cost ($)"]
).properties(title="Ticket Cost vs. Bid Price", height=250)
st.altair_chart(cost_chart, use_container_width=True)

st.divider()

st.subheader("📂 Single-Round Analysis (from CSV)")

csv_files = {
    "Demo (30 bids)":         os.path.join(DATA_DIR, "lowbid_manche_demo.csv"),
    "Multi-round 500×40":     os.path.join(DATA_DIR, "lowbid_multi_manches_500x40.csv"),
    "Stress test 200 k bids": os.path.join(DATA_DIR, "lowbid_stress_200k.csv"),
}
selected_csv = st.selectbox("Choose a dataset", list(csv_files.keys()))
csv_path = csv_files[selected_csv]

if os.path.exists(csv_path):
    bids = load_bid(csv_path)
    tree = Bid_tree()
    tree.build_tree(bids)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Bids",      tree.total_bids())
    col2.metric("Seller Revenue",  f"${tree.seller_revenue(base_cost, alpha):.2f}")
    col3.metric("Avg Cost / Bid",  f"${tree.average_cost_per_player(base_cost, alpha):.2f}")

    winner = tree.find_winner()
    if winner:
        st.success(f"🏆 Winner: **{winner.names[0]}** with price **{winner.bid}**")
    else:
        st.warning("No winner — every price was proposed by more than one player.")

    # Price distribution chart
    dist = tree.price_distribution()
    dist_df = pd.DataFrame({"Price": list(dist.keys()), "Count": list(dist.values())})
    dist_chart = alt.Chart(dist_df).mark_bar().encode(
        x=alt.X("Price:Q",  title="Bid Price"),
        y=alt.Y("Count:Q",  title="Number of Players"),
        color=alt.condition(
            alt.datum.Count == 1,
            alt.value("#22c55e"),   # green = unique
            alt.value("#ef4444")    # red   = duplicate
        ),
        tooltip=["Price", "Count"]
    ).properties(title="Price Distribution (green = unique, red = duplicate)", height=280)
    st.altair_chart(dist_chart, use_container_width=True)

    # BST tools
    with st.expander("🔍 BST Search Tools"):
        search_val = st.number_input("Search for a price", min_value=0, value=0, step=1, key="search")
        node = tree.search(int(search_val))
        if node:
            st.write(f"Found: **{node.bid}** → {node.names} ({'unique' if len(node.names)==1 else 'duplicate'})")
        else:
            st.write("Price not found in tree.")

        succ = tree.successor(int(search_val))
        pred = tree.predecessor(int(search_val))
        st.write(f"**Successor** of {search_val}: {succ.bid if succ else 'none'}")
        st.write(f"**Predecessor** of {search_val}: {pred.bid if pred else 'none'}")
else:
    st.info(f"CSV not found at `{csv_path}`. Put your CSV files in a `APP_lowbid_data/` folder next to the app.")

st.divider()

st.subheader("🎲 Multi-Round Strategy Simulation")

STRATEGY_LABELS = {
    "random":    "🎲 Random",
    "low_bias":  "📉 Low Bias",
    "mid_range": "🎯 Mid Range",
}

if run_btn or "sim_results" not in st.session_state:
    with st.spinner(f"Running {num_rounds} rounds…"):
        st.session_state["sim_results"] = cached_simulation(
            num_rounds, num_players, max_price, base_cost, alpha
        )

results = st.session_state["sim_results"]

rows = []
for s, r in results.items():
    rows.append({
        "Strategy":           STRATEGY_LABELS.get(s, s),
        "Win Rate":           f"{r['win_rate']:.1%}",
        "Avg Winning Price":  f"{r['avg_winning_price']:.1f}",
        "Avg Seller Revenue": f"${r['avg_seller_revenue']:.2f}",
        "Rounds with Winner": r['rounds_with_winner'],
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

col_a, col_b = st.columns(2)

with col_a:
    wr_df = pd.DataFrame([
        {"Strategy": STRATEGY_LABELS.get(s, s), "Win Rate": r["win_rate"]}
        for s, r in results.items()
    ])
    wr_chart = alt.Chart(wr_df).mark_bar().encode(
        x=alt.X("Strategy:N", title=None),
        y=alt.Y("Win Rate:Q", axis=alt.Axis(format="%"), title="Win Rate"),
        color=alt.Color("Strategy:N", legend=None),
        tooltip=["Strategy", alt.Tooltip("Win Rate:Q", format=".1%")]
    ).properties(title="Win Rate by Strategy", height=260)
    st.altair_chart(wr_chart, use_container_width=True)

with col_b:
    rev_df = pd.DataFrame([
        {"Strategy": STRATEGY_LABELS.get(s, s), "Avg Seller Revenue": r["avg_seller_revenue"]}
        for s, r in results.items()
    ])
    rev_chart = alt.Chart(rev_df).mark_bar().encode(
        x=alt.X("Strategy:N", title=None),
        y=alt.Y("Avg Seller Revenue:Q", title="Avg Seller Revenue ($)"),
        color=alt.Color("Strategy:N", legend=None),
        tooltip=["Strategy", alt.Tooltip("Avg Seller Revenue:Q", format="$.2f")]
    ).properties(title="Avg Seller Revenue by Strategy", height=260)
    st.altair_chart(rev_chart, use_container_width=True)

st.caption(
    "**Strategy notes:** *Random* picks uniformly. *Low Bias* uses an exponential "
    "distribution skewed toward 0. *Mid Range* uses a normal distribution centered at "
    "max_price/2. The risk premium penalises low bids, which is why Low Bias strategies "
    "generate higher seller revenue despite not winning more often."
)

st.subheader("📈 Effect of α on Seller Revenue")
with st.spinner("Computing α sensitivity (cached after first run)…"):
    alpha_df = cached_alpha_sweep(num_players, max_price, base_cost)

alpha_chart = alt.Chart(alpha_df).mark_line(point=True).encode(
    x=alt.X("Alpha:Q",              title="α (risk premium intensity)"),
    y=alt.Y("Avg Seller Revenue:Q", title="Avg Seller Revenue ($)"),
    color="Strategy:N",
    tooltip=["Alpha", "Strategy", alt.Tooltip("Avg Seller Revenue:Q", format="$.2f")]
).properties(title="Seller Revenue vs. Alpha", height=300)
st.altair_chart(alpha_chart, use_container_width=True)
