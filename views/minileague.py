import pandas as pd
import streamlit as st
import Utils.gsheet_conn as gs
import Utils.gameweek as gwk
from Utils.league import *

global ovr_data, gw_data, mn_data

# Below are the css settings for visual formatting of the metric widgets
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

# Checking for current GW and Month if complete or not and accordingly setting up a session_state param,
# which is used while populating the winnings across multiple sections of this page.
# Basically if the current GW and/or Month is not complete then it is not considered while calculating winnings
if 'gw_status' not in st.session_state:
    st.session_state['gw_status'] = gwk.get_recent_completed_gameweek()[1]
    if st.session_state['gw_status']:
        st.session_state['latest_gw'] = gwk.get_recent_completed_gameweek()[0]
    else:
        st.session_state['latest_gw'] = gwk.get_recent_completed_gameweek()[0] - 1

    mnths = gwk.get_phases()
    mnths_lst = ['August']
    st.session_state['latest_mn_last_gw'] = gwk.get_till_latest_phase()[1][1]
    # if ((not gwk.get_recent_completed_gameweek()[1]
    #      and st.session_state['latest_mn_last_gw'] == gwk.get_recent_completed_gameweek()[0]) or
    #         st.session_state['latest_mn_last_gw'] >= gwk.get_recent_completed_gameweek()[0]):
    for k, v in mnths.items():
        if k != 'Overall' and v[0] <= st.session_state['latest_gw']:
            mnths_lst.append(k)
            # st.session_state['latest_mn'] = gwk.get_till_latest_phase()[0]
    st.session_state['latest_mn'] = mnths_lst


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

    # ovr_data.loc[0, ['Rank']] = '🥇'
    # ovr_data.loc[1, ['Rank']] = '🥈'
    # ovr_data.loc[2, ['Rank']] = '🥉'
    # ovr_data.loc[3, ['Rank']] = '🏅'


data_refresh()

# Two containers for Overall Standings & Weekly, Monthly and Winnings data
_overall = st.container()
_wk_mnth = st.container(border=True)


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


# Below section is for the overall rankings container which also contains the manager metric widgets.
# The container is split into two columns, one for Overall Standings and the other for widgets

with _overall:
    # Refresh data from sheets before populating the standings. The data is cached so will only run the first time
    data_refresh()

    # Show formatted title section for the page
    st.markdown(f'<h1 style="color:#33ff33;font-size:60px;background-image:linear-gradient(45deg, #1A512E, #63A91F);"'
                f'>Leaderboard & Winnings</h1>', unsafe_allow_html=True)
    st.divider()

    # Create a space with 2 columns for overall standing and widgets respectively
    oc, mc = st.columns(2)

    # Overall Standings section
    with oc:
        st.subheader('Overall Ranking', anchor=False)
        st.caption('Select any one row using the first column for individual metrics')

        # Overall Standings data to be shown with single row selection feature enabled and store in event variable
        event = st.dataframe(
            ovr_data.style.applymap(lambda _: "background-color: Teal;", subset=([0, 1, 2, 3], slice(None))),
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
        filtered_gw_winnings['total'] = 280 / filtered_gw_winnings['Count']
        gw_winnings = filtered_gw_winnings['total'].sum()

        filtered_mn_winnings = merged_mn_df.query(
            f"Rank == 1 and Month in {st.session_state['latest_mn']}").reset_index()
        filtered_mn_winnings['total'] = 460 / filtered_mn_winnings['Count']
        mn_winnings = filtered_mn_winnings['total'].sum()

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
with _wk_mnth:
    # Below few lines are to calculate the winnings for each player till the latest completed gameweek and month
    merged_gw_winnings_df = pd.merge(gw_data, gw_data_rankers, on='Gameweek')
    merged_mn_winnings_df = pd.merge(mn_data, mn_data_rankers, on='Month')

    merged_gw_winnings_df.loc[(merged_gw_winnings_df['Rank'] == 1)
                              & (merged_gw_winnings_df['Gameweek'] <= st.session_state['latest_gw']), 'total'] \
        = 280 / merged_gw_winnings_df['Count']

    merged_gw_winnings_final = merged_gw_winnings_df.groupby('Player')['total'].sum().reset_index()

    merged_mn_winnings_df.loc[(merged_mn_winnings_df['Rank'] == 1)
                              & (merged_mn_winnings_df['Month'].isin(st.session_state['latest_mn'])), 'total'] \
        = 460 / merged_mn_winnings_df['Count']

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

    # Consider the overall winnings in calculation only during and after gameweek 38
    if gweek == 38:
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == first, 'Winnings'] += 7200
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == second, 'Winnings'] += 4500
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == third, 'Winnings'] += 3060
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == fourth, 'Winnings'] += 1500

    merged_mn_winnings_final.sort_values(by=['Winnings'], inplace=True, ascending=False)

    gwr, mnr, win = st.columns([2, 1, 1])

    # Gameweek Ranking Table section
    with gwr:
        st.subheader('Gameweek Ranking', anchor=False)
        # option = st.selectbox('Select Gameweek:', tuple(range(1, 38)), index=0)
        option = st.slider("Select Gameweek", 1, 38, gweek)
        gw_data_option = gw_data.loc[gw_data['Gameweek'] == option].sort_values(by=['Rank'])
        gw_data_option = gw_data_option.style.apply(highlight_ranker, axis=1).apply(top_row, axis=1)
        # gw_data_option.iloc[0, 2] = '🏆'
        st.write('\n')
        st.write('\n')
        st.dataframe(gw_data_option,  # .style.apply(highlight_ranker, axis=1).apply(top_row, axis=1),
                     hide_index=True, use_container_width=True,
                     column_config={'PlayerId': None},
                     column_order=['Rank', 'Player', 'Gross', 'Transfer', 'Points'], height=780)

    # Monthly Ranking Table section
    with mnr:
        st.subheader('Monthly Ranking', anchor=False)
        option1 = st.select_slider("Select Month",
                                   options=['August', 'September', 'October', 'November', 'December', 'January',
                                            'February', 'March', 'April', 'May'], value=st.session_state['latest_mn'][-1])

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
    with win:
        st.subheader('Total Winnings', anchor=False)
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.dataframe(merged_mn_winnings_final, hide_index=True, column_order=['Player', 'Winnings'], height=780,
                     column_config={'Player': st.column_config.Column(width='medium'),
                                    'Winnings': st.column_config.Column(width='small')})
