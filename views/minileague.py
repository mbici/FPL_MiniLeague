import streamlit as st
import Utils.gsheet_conn as gs


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
    st.subheader('Overall Ranking', anchor=False)
    st.dataframe(ovr_data.style.applymap(lambda _: "background-color: Teal;", subset=([0, 1, 2], slice(None))),
                 hide_index=True,  # use_container_width=True,
                 column_config={'Rank': st.column_config.Column(width='small'),
                                'Name': st.column_config.Column(width='large'),
                                'Points': st.column_config.Column(width='small')},
                 )

    st.write('\n')
    st.write('\n')
    st.write('\n')

with _wk_mnth:
    gwr, mnr = st.columns(2)
    with gwr:
        st.subheader('Gameweek Ranking', anchor=False)
        option = st.selectbox('Select Gameweek:', tuple(range(1, 38)), index=0)
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
        option = st.selectbox('Select Month:', ('August', 'September', 'October', 'November', 'December', 'January',
                                                'February', 'March', 'April', 'May'), index=0)

        mn_data_option = mn_data.loc[mn_data['Month'] == option].sort_values(by=['Rank'])
        # mn_data_option.iloc[0, 2] = '🏆'
        st.write('\n')
        st.write('\n')
        st.dataframe(mn_data_option.style.apply(highlight_ranker, axis=1).apply(top_row, axis=1),
                     hide_index=True, use_container_width=True,
                     column_order=['Rank', 'Name', 'Points'], height=610,
                     column_config={'PlayerId': None}
                     )
