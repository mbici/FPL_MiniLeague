from datetime import datetime, timedelta
import Utils.refreshData as rd
import streamlit as st
from Utils.league import *
import Utils.gsheet_conn as gs
import Utils.gameweek as gwk

st.markdown(f'<h1 style="color:#33ff33;font-size:60px;background-image:linear-gradient(45deg, #1A512E, #63A91F);"'
            f'>FPL Mini-League Details App</h1>', unsafe_allow_html=True)

# CSS styles for various elements on the screen
st.html(
    '''
    <style>
    hr {
        border-color: yellow;
    }
    </style>
    '''
)

st.markdown("""
<style>
.big-font {
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.st-emotion-cache-sesqrs {
    font-size:18px;
    color: yellow;
}
</style>
""", unsafe_allow_html=True)

st.divider()

deadline = gwk.get_upcoming_deadline()

dataDate = gs.data_load(wksheet='DataDate', cols=['DataAsOf'])
latest_gw = gwk.get_recent_completed_gameweek()
gw_state = str(latest_gw[0]) + ' ' + {latest_gw[1] == False: 'In-Progress', latest_gw[1] == True: 'Complete'}.get(True)

st.markdown(f"<p class='st-emotion-cache-sesqrs'>Gameweek {str(latest_gw[0]+1)} Deadline => {deadline}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='st-emotion-cache-sesqrs'>"
                f"Gameweek {gw_state} (Last Refreshed : {dataDate.loc[0, ['DataAsOf']].to_string(index=False)})</p>",
                unsafe_allow_html=True)
st.write('\n')

is_clicked = st.button('Refresh Data')
if is_clicked:
    with st.spinner('In-Progress......'):
        st.cache_data.clear()
        now = pd.DataFrame({'DataAsOf': [(datetime.utcnow() + timedelta(minutes=330)).strftime("%Y-%m-%d %H:%M:%S")]})
        rd.refGw()
        gs.update_data(wksheet='DataDate', df=now)

st.divider()

st.write('\n')

_help = st.container(border=True)
_mgrDetails = st.container(border=True)

# Usage Guidelines
with _help:
    st.markdown(
        """
        :green[**Usage Guidelines:**]
           - :grey[Check the Data as of notification above ☝️. If you feel the gameweek information would have been 
           updated since the date displayed, Click on 'Refresh Data' button]
           - :blue[Wait for the In-Progress spinner to disappear and do not click anywhere on the screen. It takes some 
           time to pull data from FPL servers. Once complete, 
           you will notice that Data as of is updated and it also gives the latest state of current gameweek]
           - :grey[Do not click on the refresh data button if the information is latest on the basis of data as of value]
           - :grey[Once refreshed, the app is good to use]
        
        :green[**League Statistics:**]
           - :grey[Click on this option in the sidebar navigation pane, to get information on various leaderboards and 
           winnings till date]
           - :grey[First table shows **Overall Standings**. Click in the first column (before Rank) against any 
           player in this table to get Weekly and Monthly winnings for that player]
           - :grey[The next two tables are for Gameweek and Monthly rankings. Use the slider option to choose 
           any GW and Month]
           - :grey[The last table on this page is for Total Winnings per player till date]
           
        :green[**Manager Statistics:**]
           - :grey[Click on this option in the sidebar navigation pane, to get information on manager performances 
           and analytic measures]
           - :grey[There are two sections]
             - :grey[Comparison Trends: You can choose multiple players from the dropdown box to check historical 
             year's ranks and Current Year's Rank Progression by passing gameweek]
             - :grey[Player Performance: This graph can be checked for one player at a time and gives information about 
              each gameweek's rank and points earned]
        """, unsafe_allow_html=True)

lg = league(140708)
lg_name = lg.get_league_name()

st.divider()

st.write('Support')
col1, col2 = st.columns([0.3, 4], gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/profile_image.png", width=80)

with col2:
    st.caption("Himanshu Masani")
    st.caption('FPL Admin for Fantasy Kings 2024-25')
    if st.button("✉️ Contact Me"):
        st.warning('''
                - Phone : xxxxx
                - Email : test@test.com
                ''')
