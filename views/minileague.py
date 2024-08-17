import pandas as pd
import streamlit as st
import Utils.gsheet_conn as gs
import Utils.gameweek as gwk

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


def data_refresh():
    global ovr_data, gw_data, mn_data
    ovr_data = gs.data_load('Overall', ['Rank', 'Player', 'Points']).astype({'Rank': 'int64', 'Points': 'int64'})
    gw_data = gs.data_load('Gameweek', ['Player', 'Gross', 'Transfer', 'Points', 'Rank', 'Gameweek']).astype(
        {'Rank': 'int64', 'Points': 'int64', 'Gross': 'int64', 'Transfer': 'int64'})
    mn_data = gs.data_load('Monthly', ['Player', 'Points', 'Rank', 'Month']).astype(
        {'Rank': 'int64', 'Points': 'int64'})

    ovr_data.loc[0, ['Rank']] = '🥇'
    ovr_data.loc[1, ['Rank']] = '🥈'
    ovr_data.loc[2, ['Rank']] = '🥉'
    ovr_data.loc[3, ['Rank']] = '🏅'


data_refresh()

_overall = st.container()
_wk_mnth = st.container(border=True)
_refresh = st.container(border=True)
global ovr_data, gw_data, mn_data


def style_dataframe(df):
    return df.style.set_table_styles(
        [{
            'selector': 'th',
            'props': [
                ('background-color', '#4CAF50'),
                ('color', 'white'),
                ('font-family', 'Arial, sans-serif'),
                ('font-size', '16px')
            ]
        },
            {
                'selector': 'td, th',
                'props': [
                    ('border', '2px solid #4CAF50')
                ]
            }]
    )


def highlight_ranker(row):
    return ['background-color: Teal;'] * len(row) if row.Rank == 1 else ['background-color: '] * len(row)


def top_row(row):
    return ['font-size: 100pt'] * len(row) if row.Rank == 1 else ['font-size: '] * len(row)


with _overall:
    data_refresh()
    st.markdown(f'<h1 style="color:#33ff33;font-size:60px;background-image:linear-gradient(45deg, #1A512E, #63A91F);"'
                f'>Leaderboard & Winnings</h1>', unsafe_allow_html=True)
    # st.title(f'{lg_name} - Statistics', anchor=False)
    st.divider()

    oc, mc = st.columns(2)
    with oc:
        st.subheader('Overall Ranking', anchor=False)
        st.caption('Select any one row using the first column for individual metrics')
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
        personC = {len(selection) == 0: '**Select a player first**', len(selection) > 0: personC}.get(True)

        filtered_data_gw = gw_data.query("Player == '{0}'".format(person)).reset_index().sort_values('Gameweek')
        filtered_data_mn = mn_data.query("Player == '{0}'".format(personC)).reset_index()

        gw_data_rankers = gw_data[gw_data['Rank'] == 1].groupby('Gameweek').size().reset_index(name='Count') \
            .sort_values('Gameweek')
        mn_data_rankers = mn_data[mn_data['Rank'] == 1].groupby('Month').size().reset_index(name='Count')
        # st.write(gw_data_rankers)

        merged_gw_df = pd.merge(filtered_data_gw, gw_data_rankers, on='Gameweek')
        merged_mn_df = pd.merge(filtered_data_mn, mn_data_rankers, on='Month')

        filtered_gw_winnings = merged_gw_df.query('Rank == 1').reset_index()
        filtered_gw_winnings['total'] = 280 / filtered_gw_winnings['Count']
        gw_winnings = filtered_gw_winnings['total'].sum()

        filtered_mn_winnings = merged_mn_df.query('Rank == 1').reset_index()
        filtered_mn_winnings['total'] = 460 / filtered_mn_winnings['Count']
        mn_winnings = filtered_mn_winnings['total'].sum()

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

            st.metric('Weekly Winnings', '₹' + str(gw_winnings))
            st.markdown(2 * "<br />", unsafe_allow_html=True)
            st.metric('Monthly Winnings', '₹' + str(mn_winnings))

    st.write('\n')
    st.write('\n')
    st.write('\n')

with _wk_mnth:
    merged_gw_winnings_df = pd.merge(gw_data, gw_data_rankers, on='Gameweek')
    merged_mn_winnings_df = pd.merge(mn_data, mn_data_rankers, on='Month')

    merged_gw_winnings_df.loc[merged_gw_winnings_df['Rank'] == 1, 'total'] = 280 / merged_gw_winnings_df['Count']
    merged_gw_winnings_final = merged_gw_winnings_df.groupby('Player')['total'].sum().reset_index()

    merged_mn_winnings_df.loc[merged_mn_winnings_df['Rank'] == 1, 'total'] = 460 / merged_mn_winnings_df['Count']
    merged_mn_winnings_final = merged_mn_winnings_df.groupby('Player')['total'].sum().reset_index()
    merged_mn_winnings_final = merged_mn_winnings_final.append(merged_gw_winnings_final)
    merged_mn_winnings_final = merged_mn_winnings_final.groupby(merged_mn_winnings_final['Player'])['total'] \
        .sum().reset_index()
    merged_mn_winnings_final.rename(columns={'total': 'Winnings'}, inplace=True)

    first = ovr_data.loc[0, ['Player']].to_string(index=False)
    second = ovr_data.loc[1, ['Player']].to_string(index=False)
    third = ovr_data.loc[2, ['Player']].to_string(index=False)
    fourth = ovr_data.loc[3, ['Player']].to_string(index=False)

    gweek = gwk.get_recent_completed_gameweek()[0]  #### uncomment this after gameweek1
    if gweek == 38:
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == first, 'Winnings'] += 7200
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == second, 'Winnings'] += 4500
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == third, 'Winnings'] += 3060
        merged_mn_winnings_final.loc[merged_mn_winnings_final['Player'] == fourth, 'Winnings'] += 1500

    merged_mn_winnings_final.sort_values(by=['Winnings'], inplace=True, ascending=False)

    gwr, mnr, win = st.columns([2, 1, 1])
    with gwr:
        st.subheader('Gameweek Ranking', anchor=False)
        # option = st.selectbox('Select Gameweek:', tuple(range(1, 38)), index=0)
        option = st.slider("Select Gameweek", 1, 38, 1)
        gw_data_option = gw_data.loc[gw_data['Gameweek'] == option].sort_values(by=['Rank'])
        gw_data_option = gw_data_option.style.apply(highlight_ranker, axis=1).apply(top_row, axis=1)
        # gw_data_option.iloc[0, 2] = '🏆'
        st.write('\n')
        st.write('\n')
        st.dataframe(gw_data_option,  # .style.apply(highlight_ranker, axis=1).apply(top_row, axis=1),
                     hide_index=True, use_container_width=True,
                     column_config={'PlayerId': None},
                     column_order=['Rank', 'Player', 'Gross', 'Transfer', 'Points'], height=780)

    with mnr:
        st.subheader('Monthly Ranking', anchor=False)
        # option = st.selectbox('Select Month:', ('August', 'September', 'October', 'November', 'December', 'January',
        #                                        'February', 'March', 'April', 'May'), index=0)
        option1 = st.select_slider("Select Month",
                                   options=['August', 'September', 'October', 'November', 'December', 'January',
                                            'February', 'March', 'April', 'May'])

        mn_data_option = mn_data.loc[mn_data['Month'] == option1].sort_values(by=['Rank'])
        # mn_data_option.iloc[0, 2] = '🏆'
        st.write('\n')
        st.write('\n')
        st.dataframe(mn_data_option.style.apply(highlight_ranker, axis=1).apply(top_row, axis=1),
                     hide_index=True, use_container_width=True,
                     column_order=['Rank', 'Player', 'Points'], height=780,
                     column_config={'PlayerId': None}
                     )

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
