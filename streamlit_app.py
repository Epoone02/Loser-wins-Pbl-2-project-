import streamlit as st

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

