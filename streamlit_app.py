import streamlit as st

st.title('Welcome to Abracadabra')
st.write('description')

if st.button('Start Bidding!'):
    st.switch_page('Loser-wins-Pbl-2-project-/pages/PlayerVSPlayer.py')

if st.button('See Stats'):
    st.switch_page('Loser-wins-Pbl-2-project-/pages/Chart.py')


