import streamlit as st

<<<<<<< HEAD
st.set_page_config(page_title="LowBid Auction", page_icon="🔨")

st.title('Welcome to Abracadabra 🎩')
st.write('''
Welcome to the LowBid auction platform. 
The rules are simple: the winner is the person who proposes the **lowest unique price**.
But beware: the lower you bid, the more expensive the ticket costs!
''')

if st.button('Start Bidding!', type="primary"):
    st.switch_page('pages/PlayerVSPlayer.py')

if st.button('See Stats'):
    st.switch_page('pages/Chart.py')
=======
st.set_page_config(page_title="Abracadabra - LowBid", page_icon="🔨", layout="centered")

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

>>>>>>> 2ddfc4c5965dfe097f2ca7874b61e5b285c16184

