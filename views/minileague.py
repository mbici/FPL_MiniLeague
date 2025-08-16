import pandas as pd
import streamlit as st
import Utils.gsheet_conn as gs
import Utils.gameweek as gwk
from Utils.league import *

global ovr_data, gw_data, mn_data

#css settings for visual formatting of the metric widgets
css = '''
            [data-testid="stMetric"] {
                width: 250px;
                height: 120px;
                margin: auto;
                overflow-wrap: break-word;
                white-space: break-spaces;
                color: white;
                
            }

            [data-testid="stMetricValue"] > div {
                width: fit-content;
                margin: auto;
                overflow-wrap: break-word;
                white-space: break-spaces;
                font-size: 50px;
                color: #35e8d9;
            }
            
            [data-testid="stMetricDelta"] {
                width: fit-content;
                margin: auto;
                overflow-wrap: break-word;
                white-space: break-spaces;
                font-size: 20px;
            }
            
            [data-testid="stMetricLabel"] {
                width: fit-content;
                margin: auto;
                overflow-wrap: break-word;
                white-space: break-spaces;
                color: yellow;
            }

            [data-testid="stMetricLabel"] > div > div > p {
                font-size: 25px;
                width: fit-content;
                margin: auto;
                overflow-wrap: break-word;
                white-space: break-spaces;
                color: yellow;
            }
            '''

#Updated datafraeme styles
st.markdown("""
    <style>
    /* Fancy DataFrame container styling */
    .stDataFrame, .stTable {
        border-radius: 18px !important;
        box-shadow: 0 6px 32px rgba(51,255,51,0.10), 0 1.5px 8px rgba(51,255,51,0.08);
        background: linear-gradient(90deg, #f8f7f3 0%, #ecebe4 80%, #e2e1d9 100%) !important;
        border: 2px solid #ecebe4 !important;
        margin-bottom: 18px;
        overflow: hidden;
    }
    .stDataFrame table {
        font-size: 1.08rem;
        border-radius: 12px;
        overflow: hidden;
    }
    .stDataFrame th {
        background: #33ff33 !important;
        color: #124010 !important;
        font-size: 1.18rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #ecebe4 !important;
    }
    .stDataFrame td {
        background: rgba(245,245,240,0.12) !important;
        color: #222 !important;
        border-bottom: 1px solid #ecebe4 !important;
        transition: background 0.2s;
    }
    .stDataFrame tr:hover td {
        background: #eaffea !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Updated tab styling - removed gradient background and set to full width
st.markdown("""
<style>
/* Modern glassmorphism tab styling */
.stTabs {
    background: transparent;
    margin-top: 24px;
    width: 100%;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 18px;
    /* match the page background so the tabs container blends with the app theme */
    background: rgba(71,155,41,0.15) !important;
    border-radius: 20px;
    /* soften the outer shadow since background is translucent */
    box-shadow: 0 8px 32px rgba(51,255,51,0.12), 0 2px 8px rgba(51,255,51,0.10);
    padding: 14px 0px;
    width: 100%;
    display: flex;
    justify-content: space-between;
    backdrop-filter: blur(12px);
    border: none;
}
.stTabs [data-baseweb="tab"] {
    height: 54px;
    color: #f3f3f3;
    /* darker grey background for inactive tabs */
    background: linear-gradient(120deg, #9a9a9a 0%, #6f6f6f 100%);
    border-radius: 14px;
    font-weight: 600;
    margin: 0;
    padding: 0px 36px;
    border: 1px solid rgba(0,0,0,0.14);
    transition: all 0.25s cubic-bezier(.4,0,.2,1);
    flex-grow: 1;
    text-align: center;
    font-size: 1.22rem;
    box-shadow: 0 2px 12px rgba(51,255,51,0.06);
    letter-spacing: 0.7px;
    position: relative;
    cursor: pointer;
    backdrop-filter: blur(2px);
    opacity: 0.92;
}
.stTabs [data-baseweb="tab"] button,
.stTabs [data-baseweb="tab"] > button {
    background: transparent !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:not(:last-child) {
    /* subtle divider on the right edge of each tab except the last */
    position: relative;
}
.stTabs [data-baseweb="tab"]:not(:last-child):after {
    content: '';
    position: absolute;
    right: 0;
    top: 18%;
    height: 64%;
    width: 1px;
    background: rgba(0,0,0,0.06);
    transform: translateX(0.5px);
    border-radius: 1px;
}
.stTabs [data-baseweb="tab"]:hover {
    background: linear-gradient(120deg, #eaffea 60%, #d6f5d6 100%);
    color: #1a512e;
    box-shadow: 0 6px 18px rgba(51,255,51,0.18);
    border: 1.5px solid #33ff33;
    opacity: 1;
    transform: scale(1.04);
}
.stTabs [aria-selected="true"] {
    /* Brighter distinct highlight for the selected tab */
    background: linear-gradient(90deg, #33ff77 0%, #a8ffd0 40%, #eaffea 100%);
    color: #053212; /* darker text for contrast */
    font-weight: 800;
    font-size: 1.38rem;
    /* main shadow + thin outline glow for selected state */
    box-shadow: 0 12px 36px rgba(51,255,51,0.22), 0 0 0 3px rgba(51,255,51,0.08);
    border: 2.5px solid rgba(0,200,83,0.95);
    position: relative;
    z-index: 2;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px rgba(255,255,255,0.12);
    filter: brightness(1.05);
    opacity: 1;
    transform: scale(1.09);
    transition: all 0.22s cubic-bezier(.4,0,.2,1);
}
.stTabs [aria-selected="true"]:before {
    content: '⚽';
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.25rem;
    color: #b3a369;
    filter: drop-shadow(0 0 2px #ecebe4);
}
button:focus {
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

# Function to refresh data from the googlesheets containing the GW, Monthly and Overall standings and points
def data_refresh():
    """
    Function to refresh data from the googlesheets containing the GW, Monthly and Overall standings and points
    :return:
    """
    global ovr_data, gw_data, mn_data

    # Read data from various sheets into the globally defined variables. This data is for overall, GW and monthly
    ovr_data = gs.data_load('Overall', ['Rank', 'Player', 'Points', 'Last_Rank']) \
        .astype({'Rank': 'int64', 'Last_Rank': 'int64', 'Points': 'int64'})
    gw_data = gs.data_load('Gameweek', ['Player', 'Gross', 'Transfer', 'Points', 'Rank', 'Gameweek']) \
        .astype({'Rank': 'int64', 'Points': 'int64', 'Gross': 'int64', 'Transfer': 'int64'})
    mn_data = gs.data_load('Monthly', ['Player', 'Points', 'Rank', 'Month']) \
        .astype({'Rank': 'int64', 'Points': 'int64'})

mths_lst_winning = ['0']
# Checking for current GW and Month if complete or not and accordingly setting up a session_state param,
# which is used while populating the winnings across multiple sections of this page.
# If the current GW and/or Month is not complete then it is not considered while calculating winnings
if 'gw_status' not in st.session_state:
    cgwk = gwk.get_recent_completed_gameweek()[0]
    st.session_state['gw_status'] = gwk.get_recent_completed_gameweek()[1]
    if st.session_state['gw_status']:
        st.session_state['latest_gw'] = cgwk  # gwk.get_recent_completed_gameweek()[0]
    else:
        st.session_state['latest_gw'] = cgwk - 1  # gwk.get_recent_completed_gameweek()[0] - 1

    mnths = gwk.get_phases()
    mnths_lst = ['August']
    mnths_lst_slider = ['August']

    st.session_state['latest_mn_last_gw'] = gwk.get_till_latest_phase()[1][1]

    for k, v in mnths.items():
        if k != 'Overall' and v[1] <= st.session_state['latest_gw']:
            mnths_lst.append(k)
            mths_lst_winning.append(k)
        if k != 'Overall' and v[0] <= cgwk:
            mnths_lst_slider.append(k)
    st.session_state['latest_mn'] = mnths_lst
    st.session_state['latest_mn_slider'] = mnths_lst_slider

    # ovr_data.loc[0, ['Rank']] = '🥇'
    # ovr_data.loc[1, ['Rank']] = '🥈'
    # ovr_data.loc[2, ['Rank']] = '🥉'
    # ovr_data.loc[3, ['Rank']] = '🏅'


data_refresh()

# Two containers for Overall Standings & Weekly, Monthly and Winnings data
# _overall = st.container()
# _wk_mnth = st.container(border=True)


def highlight_ranker(row):
    """
    Function to highlight the background of row with Rank value 1 with Teal color
    :param row: pandas dataframe row
    :return: value for pandas' style apply method
    """
    return ['background-color: Teal;'] * len(row) if row.Rank == 1 else ['background-color: '] * len(row)


def top_row(row):
    """
    Function to change font-size of row with Rank value 1.
    :param row: pandas dataframe row
    :return: value for pandas' style apply method
    """
    return ['font-size: 100pt'] * len(row) if row.Rank == 1 else ['font-size: '] * len(row)

# Show formatted title section for the page
st.markdown(f'<h1 style="color:#33ff33;font-size:60px;background-image:linear-gradient(45deg, #1A512E, #63A91F);font-family:Montserrat;text-align:left;padding:20px;border-radius:10px;"'
                f'>Leaderboard & Winnings</h1>', unsafe_allow_html=True)
st.divider()

# Create tabs for Overall, Gameweek, Monthly and Winnings sections
tab_ovr, tab_gw, tab_mn, tab_winnings = st.tabs(['Overall Standings', 'Gameweek Ranking', 'Monthly Ranking', 'Total Winnings'])

with tab_ovr:
# Below section is for the overall rankings container which also contains the manager metric widgets.
# The container is split into two columns, one for Overall Standings and the other for widgets

    # Create a space with 2 columns for overall standing and widgets respectively
    oc, mc = st.columns(2)

    # Overall Standings section
    with oc:
        st.subheader('Overall Ranking', anchor=False)
        st.caption('Select any one row using the first column for individual metrics')

        # Overall Standings data to be shown with single row selection feature enabled and store in event variable
        event = st.dataframe(
            ovr_data.style.map(lambda _: "background-color: Teal;", subset=([0, 1, 2, 3], slice(None))),
            hide_index=True,  # use_container_width=True,
            column_config={'Rank': st.column_config.Column(width='small'),
                        'Player': st.column_config.Column(width='large'),
                        'Points': st.column_config.Column(width='small')},
            column_order=['Rank', 'Player', 'Points'],
            on_select="rerun",
            selection_mode="single-row"
        )

        selection = event.selection.rows
        person = ovr_data.iloc[selection]['Player'].to_string(index=False)
        personC = person.split(' ')[0].capitalize() + ' ' + person.split(' ')[1].capitalize()

        # In case the selection is None then a static text to be displayed above the widgets section else selected name
        personC = {len(selection) == 0: '***Select a player***', len(selection) > 0: personC}.get(True)

        # Below lines are basically filtering the gameweek and monthly dataframes for the selected manager name
        # Then if the manager has attained rank #1 against any gameweek and/or month, it is considered
        # to calculate the eventual winning amount till date for that manager, barring any ongoing month and/or gw

        filtered_data_gw = gw_data.query("Player == '{0}'".format(person)).reset_index().sort_values('Gameweek')
        filtered_data_mn = mn_data.query("Player == '{0}'".format(personC)).reset_index()

        gw_data_rankers = gw_data[gw_data['Rank'] == 1].groupby('Gameweek').size().reset_index(name='Count') \
            .sort_values('Gameweek')
        mn_data_rankers = mn_data[mn_data['Rank'] == 1].groupby('Month').size().reset_index(name='Count')

        merged_gw_df = pd.merge(filtered_data_gw, gw_data_rankers, on='Gameweek')
        merged_mn_df = pd.merge(filtered_data_mn, mn_data_rankers, on='Month')

        filtered_gw_winnings = merged_gw_df.query(
            f"Rank == 1 and Gameweek<={st.session_state['latest_gw']}").reset_index()
        filtered_gw_winnings['total'] = 300 / filtered_gw_winnings['Count']
        gw_winnings = {filtered_gw_winnings['total'].sum()>0: filtered_gw_winnings['total'].sum(),
                       filtered_gw_winnings['total'].sum() == 0: 0}.get(True)

        filtered_mn_winnings = merged_mn_df.query(
            f"Rank == 1 and Month in {mths_lst_winning}").reset_index()
        filtered_mn_winnings['total'] = 530 / filtered_mn_winnings['Count']
        mn_winnings = {filtered_mn_winnings['total'].sum()>0: filtered_mn_winnings['total'].sum(),
                       filtered_mn_winnings['total'].sum() == 0: 0}.get(True)

        # Metric Widgets section
    with mc:
        st.markdown(1 * "<br />", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: white;'>{personC}</h4>", unsafe_allow_html=True)
        st.subheader('', anchor=False, divider='rainbow')
        st.markdown(1 * "<br />", unsafe_allow_html=True)

        if gw_winnings is not None:
            st.markdown(f"""
            <style>
            {css}
            </style>
            """, unsafe_allow_html=True)

            g, m = st.columns(2)
            with g:
                st.metric('Weekly Winnings', '₹ ' + str(gw_winnings))

            with m:
                st.metric('Monthly Winnings', '₹ ' + str(mn_winnings))

            st.markdown(2 * "<br />", unsafe_allow_html=True)

            st.metric('Rank', {len(selection) > 0: ovr_data.loc[ovr_data['Player'] == personC, 'Rank']
                    .to_string(index=False)}.get(True),
                    delta=int({len(selection) > 0: ovr_data.loc[ovr_data['Player'] == personC, 'Last_Rank']
                    .to_string(index=False)}.get(True, 0)) -
                            int({len(selection) > 0: ovr_data.loc[ovr_data['Player'] == personC, 'Rank']
                    .to_string(index=False)}.get(True, 0)),
                    delta_color='normal')

    st.write('\n')
    st.write('\n')
    st.write('\n')


# Weekly, Monthly and Winnings table section
# Below few lines are to calculate the winnings for each player till the latest completed gameweek and month
merged_gw_winnings_df = pd.merge(gw_data, gw_data_rankers, on='Gameweek')
merged_mn_winnings_df = pd.merge(mn_data, mn_data_rankers, on='Month')

merged_gw_winnings_df.loc[(merged_gw_winnings_df['Rank'] == 1)
                            & (merged_gw_winnings_df['Gameweek'] <= st.session_state['latest_gw']), 'total'] \
    = 300 / merged_gw_winnings_df['Count']

merged_gw_winnings_final = merged_gw_winnings_df.groupby('Player')['total'].sum().reset_index()

merged_mn_winnings_df.loc[(merged_mn_winnings_df['Rank'] == 1)
                            & (merged_mn_winnings_df['Month'].isin(mths_lst_winning)), 'total'] \
    = 530 / merged_mn_winnings_df['Count']

merged_mn_winnings_final = merged_mn_winnings_df.groupby('Player')['total'].sum().reset_index()
merged_mn_winnings_final = pd.concat([merged_mn_winnings_final, merged_gw_winnings_final], ignore_index=True)
merged_mn_winnings_final = merged_mn_winnings_final.groupby(merged_mn_winnings_final['Player'])['total'] \
    .sum().reset_index()
merged_mn_winnings_final.rename(columns={'total': 'Winnings'}, inplace=True)

first = ovr_data.loc[0, ['Player']].to_string(index=False)
second = ovr_data.loc[1, ['Player']].to_string(index=False)
third = ovr_data.loc[2, ['Player']].to_string(index=False)
fourth = ovr_data.loc[3, ['Player']].to_string(index=False)

gweek = gwk.get_recent_completed_gameweek()[0]
gweekStatus = gwk.get_recent_completed_gameweek()[1]

# Consider the overall winnings in calculation only during and after gameweek 38
if gweek == 38 and gweekStatus:
    merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == first, 'Winnings'] += 7200
    merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == second, 'Winnings'] += 4500
    merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == third, 'Winnings'] += 3060
    merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == fourth, 'Winnings'] += 1500

merged_mn_winnings_final.sort_values(by=['Winnings'], inplace=True, ascending=False)

    # gwr, mnr, win = st.columns([2, 1, 1])
with tab_gw:
    # Gameweek Ranking Table section
    # with gwr:
    st.subheader('Gameweek Ranking', anchor=False)
    option = st.slider("Select Gameweek", 1, 38, gweek, label_visibility='collapsed')
    gw_data_option = gw_data.loc[gw_data['Gameweek'] == option].sort_values(by=['Rank'])
    gw_data_option = gw_data_option.style.apply(highlight_ranker, axis=1).apply(top_row, axis=1)
    st.write('\n')
    st.write('\n')

    st.dataframe(
        gw_data_option,
        hide_index=True,
        use_container_width=True,
        column_config={'PlayerId': None},
        column_order=['Rank', 'Player', 'Gross', 'Transfer', 'Points'],
        height=780
    )

# Monthly Ranking Table section
with tab_mn:
    st.subheader('Monthly Ranking', anchor=False)
    option1 = st.select_slider("Select Month", label_visibility='collapsed',
                                options=['August', 'September', 'October', 'November', 'December', 'January',
                                        'February', 'March', 'April', 'May'],
                                value=st.session_state['latest_mn_slider'][-1])

    mn_data_option = mn_data.loc[mn_data['Month'] == option1].sort_values(by=['Rank'])
    # mn_data_option.iloc[0, 2] = '🏆'
    st.write('\n')
    st.write('\n')
    st.dataframe(mn_data_option.style.apply(highlight_ranker, axis=1).apply(top_row, axis=1),
                    hide_index=True, use_container_width=True,
                    column_order=['Rank', 'Player', 'Points'], height=780,
                    column_config={'PlayerId': None}
                    )

# Winnings Table section
with tab_winnings:
    st.subheader('Total Winnings', anchor=False)
    st.dataframe(merged_mn_winnings_final, hide_index=True, column_order=['Player', 'Winnings'], height=780,
                    column_config={'Player': st.column_config.Column(width='medium'),
                                'Winnings': st.column_config.Column(width='small')})
