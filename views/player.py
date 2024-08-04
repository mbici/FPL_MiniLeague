import streamlit as st
from league import *
import plyr_history as ph

st.title("Player Details")
st.write("\n")
lg = league(140708)

plyrs = lg.get_league_players()

plr_entry_link = [{p['player']:p['id']} for p in plyrs]
plyr_list = [p['player'] for p in plyrs]
option = st.selectbox('Player:', tuple(plyr_list), index=None)
st.write('\n\n')

if option is None:
    option = ''

st.write(f"**Ranking Trend for {option} by year**\n")

for i in plr_entry_link:
    if option in i:
        val = i[option]
        data = ph.plyr_hist(val)
        data = data.set_index("Season")

        st.bar_chart(data, x_label='Season', y_label='Rank')
        break





