import streamlit as st
from Utils.league import *
import plyr_history as ph
import pandas as pd
from streamlit import session_state as session_state
import Utils.gsheet_conn as gs
import altair as alt


lg = league(140708)

st.markdown(f'<h1 style="color:#33ff33;font-size:60px;background-image:linear-gradient(45deg, #1A512E, #63A91F);"'
                f'>Manager Details</h1>', unsafe_allow_html=True)
st.divider()
plyrs = lg.get_league_players()

plr_entry_link = [{p['Player']: p['Id']} for p in plyrs]
plyr_lst = pd.DataFrame.from_records(plyrs).get('Player')
#session_state['plyr_lst'] = plyr_lst

gw_data = gs.data_load('Gameweek', ['Player', 'Points', 'Gameweek']).astype(
            {'Points': 'int64', 'Gameweek': 'int64'})
gw_data['Players'] = [x.split(' ')[0].capitalize() + ' ' + x.split(' ')[1].capitalize() for x in gw_data['Player']]
gw_data_cum = gw_data.groupby(['Player', 'Players', 'Gameweek']).sum().groupby(level=0).cumsum()
gw_data_cum['Rank'] = gw_data_cum.groupby(['Gameweek'])['Points'].rank(method='dense', ascending=False)

#gw_data_cum['Player'] = gw_data_cum.apply(lambda row: row['Player'].split(' ')[0].capitalize() + ' '
#                              + row['Player'].split(' ')[1].capitalize(), axis=1)


def button_state():
    if 'button_sent' not in session_state:
        session_state['button_sent'] = False

_container1 = st.container(border=True)

with _container1:
    option = st.multiselect(label='Select Players', options=plyr_lst, on_change=button_state(),
                            placeholder="Choose Player(s)", label_visibility='collapsed', default=plyr_lst[0])
    session_state['button_sent'] = False
    button_sent = st.button("SUBMIT")
    col1, col2 = st.columns(2)

    with col1:
        if button_sent:
            session_state['button_sent'] = True
            if option is None:
                option = ''
            else:
                data = ph.plyr_hist([p[i] for i in option for p in plr_entry_link if i in p], plr_entry_link)

        st.write('\n')

        st.subheader("**Ranking Trend by year**\n", anchor=False)
        st.write('\n')

        if session_state['button_sent']:
            st.bar_chart(data, x="Season", y="Rank", color='Player Name', stack=False)

    with col2:
        gw_data_option = gw_data_cum.query(f'Players in {option}').reset_index()
        st.write('\n')
        st.subheader("**Ranking Trend by Gameweek - Current Year**\n", anchor=False)
        # if session_state['button_sent']:
        #     st.line_chart(data=gw_data_option, x='Gameweek', y='Rank', color='Players')
        #
        # chart = alt.Chart(gw_data_option).mark_line(point=True).encode(
        #     x=alt.X("Gameweek:O", title="Gameweek"),
        #     #y="rank:O",
        #     y=alt.Y("Rank:N", title="Rank"),
        #     color=alt.Color("Players:N")
        # ).properties(
        #     title="GW Rank",
        #     width=800,
        #     height=400
        # )
        #
        # st.altair_chart(chart, use_container_width=True)

        if session_state['button_sent']:
            chart1 = alt.Chart(gw_data_option).mark_line(point=True).encode(
                x=alt.X('Gameweek', scale=alt.Scale(reverse=False), axis=alt.Axis(grid=False)),  # Reverse the x-axis
                y=alt.Y('Rank', scale=alt.Scale(reverse=True), axis=alt.Axis(grid=True, tickCount=9)),
                color=alt.Color("Players", legend=alt.Legend(orient='bottom'))
            ).properties(
               # title='GW Rank',
                width=580,
                height=350
            )

            st.altair_chart(chart1, use_container_width=True)