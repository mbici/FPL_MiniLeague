import pandas as pd
import streamlit as st
import Utils.gsheet_conn as gs

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
    ovr_data = gs.data_load('Overall', ['Rank', 'Name', 'Points']).astype({'Rank': 'int64', 'Points': 'int64'})
    gw_data = gs.data_load('Gameweek', ['Player', 'Points', 'Rank', 'Gameweek']).astype(
        {'Rank': 'int64', 'Points': 'int64'})
    mn_data = gs.data_load('Monthly', ['Name', 'Points', 'Rank', 'Month']).astype({'Rank': 'int64', 'Points': 'int64'})

    ovr_data.loc[0, ['Rank']] = '🥇'
    ovr_data.loc[1, ['Rank']] = '🥈'
    ovr_data.loc[2, ['Rank']] = '🥉'


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


with _refresh:
    if st.button('Refresh Data'):
        st.cache_data.clear()
        data_refresh()

with _overall:
    data_refresh()
    st.markdown(f'<h1 style="color:#33ff33;font-size:60px;background-image:linear-gradient(45deg, #1A512E, #63A91F);"'
                f'>Fantasy Kings 2024/25 - Statistics</h1>', unsafe_allow_html=True)
    # st.title(f'{lg_name} - Statistics', anchor=False)
    st.divider()

    oc, mc = st.columns(2)
    with oc:
        st.subheader('Overall Ranking', anchor=False)
        st.caption('Select any one row using the first column for individual metrics')
        event = st.dataframe(
            ovr_data.style.applymap(lambda _: "background-color: Teal;", subset=([0, 1, 2], slice(None))),
            hide_index=True,  # use_container_width=True,
            column_config={'Rank': st.column_config.Column(width='small'),
                           'Name': st.column_config.Column(width='large'),
                           'Points': st.column_config.Column(width='small')}, on_select="rerun",
            selection_mode="single-row"
        )

        selection = event.selection.rows
        person = ovr_data.iloc[selection]['Name'].to_string(index=False)
        personC = person.split(' ')[0].capitalize() + ' ' + person.split(' ')[1].capitalize()

        filtered_data_gw = gw_data.query("Player == '{0}'".format(person)).reset_index().sort_values('Gameweek')
        filtered_data_mn = mn_data.query("Name == '{0}'".format(personC)).reset_index()

        # st.write(filtered_data_gw)
        # gw_data['Rankers'] = gw_data.groupby(['Gameweek'])[]
        # st.write(gw_data.filter(lambda x : x['Rank']==1))
        # gw_data_rankers = gw_data.groupby(['Gameweek']).count().reset_index()
        gw_data_rankers = gw_data[gw_data['Rank'] == 1].groupby('Gameweek').size().reset_index(
            name='Count').sort_values(
            'Gameweek')
        mn_data_rankers = mn_data[mn_data['Rank'] == 1].groupby('Month').size().reset_index(name='Count')
        # st.write(gw_data_rankers)

        merged_gw_df = pd.merge(filtered_data_gw, gw_data_rankers, on='Gameweek')
        merged_mn_df = pd.merge(filtered_data_mn, mn_data_rankers, on='Month')

        filtered_gw_winnings = merged_gw_df.query('Rank == 1').reset_index()
        filtered_gw_winnings['total'] = 221 / filtered_gw_winnings['Count']
        gw_winnings = filtered_gw_winnings['total'].sum()

        filtered_mn_winnings = merged_mn_df.query('Rank == 1').reset_index()
        filtered_mn_winnings['total'] = 360 / filtered_mn_winnings['Count']
        mn_winnings = filtered_mn_winnings['total'].sum()

    with mc:
        st.markdown(4 * "<br />", unsafe_allow_html=True)

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
    gwr, mnr = st.columns(2)
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
                     column_order=['Rank', 'Player', 'Points'], height=610)

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
                     column_order=['Rank', 'Name', 'Points'], height=610,
                     column_config={'PlayerId': None}
                     )
