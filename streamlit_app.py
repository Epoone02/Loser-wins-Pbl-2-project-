import streamlit as st

st.set_page_config(page_title="Winabid - LowBid", page_icon="🔨", layout="centered")

st.title("Welcome to Winabid")
st.subheader("The Lowest Unique Bid Wins!")

st.markdown("""
### How it works
- Every player places a **bid** (integer ≥ 0).
- The **winner** is the player with the **lowest price that no one else chose**.
- The **host** can add bot players and resolve the round at any time.
            
NOW lets start bidding! (its not real money so its okay )
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Start Bidding!", use_container_width=True):
        st.switch_page("pages/PlayerVSPlayer.py")

with col2:
    if st.button("See Stats & Simulation", use_container_width=True):
        st.switch_page("pages/Chart.py")


