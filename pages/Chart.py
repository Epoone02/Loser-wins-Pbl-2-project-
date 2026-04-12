import streamlit as st
import pandas as pd
from PlayerVSPlayer import wins

st.title('Here are the stats:')

df = pd.DataFrame(wins, columns = 'Latest wins')

if wins is not []:
    st.line_chart(df, x = 'Latest Wins', y = 'Price')
else:
    st.info("No data!")
