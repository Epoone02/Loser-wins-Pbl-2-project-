import streamlit as st
from main import Bid_tree

@st.cache_resource
def get_shared_game_state():
    return [0,[],None]

game_state = get_shared_game_state()

result = False

query_params = st.query_params
is_host = query_params.get("role") == "host"

if is_host:
    st.title("Host Dashboard")
    st.write(f"Total bids received so far: {game_state[0]}")
    if st.button("Start"):
        round = Bid_tree()
        round.build_tree(game_state[1])
        st.write(f'The winner is : {round.minBST()[0]}!')
        
else:
    st.title("Player Screen")
    player_name = st.text_input("Your Name")
    bid = st.number_input("Your Bid:", min_value=0)
    
    if st.button("Place Bid"):
        game_state[0] += 1
        game_state[1].append([player_name, bid])
        st.success("Bid sent to the host!")
    