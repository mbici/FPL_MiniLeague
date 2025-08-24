import streamlit as st
import Utils.gsheet_conn as gs
import pandas as pd
# from fpl_streamlit_app import latest_gw, completed_months

# Function to refresh data from the googlesheets containing the GW, Monthly and Overall standings and points
@st.cache_data()
def data_refresh():
    """
    Function to refresh data from the googlesheets containing the GW, Monthly and Overall standings and points
    :return:
    """

    # Read data from various sheets into the globally defined variables. This data is for overall, GW and monthly
    ovr_data = gs.data_load('Overall', ['Rank', 'Player', 'Points', 'Last_Rank']) \
        .astype({'Rank': 'int64', 'Last_Rank': 'int64', 'Points': 'int64'})
    gw_data = gs.data_load('Gameweek', ['Player', 'Gross', 'Transfer', 'Points', 'Rank', 'Gameweek']) \
        .astype({'Rank': 'int64', 'Points': 'int64', 'Gross': 'int64', 'Transfer': 'int64'})
    mn_data = gs.data_load('Monthly', ['Player', 'Points', 'Rank', 'Month']) \
        .astype({'Rank': 'int64', 'Points': 'int64'})
    
    return ovr_data, gw_data, mn_data

@st.cache_data()
def winnings_data(gw_data, mn_data):
    """
    Function to calculate the winnings across the mini league
    :return: DataFrame of winnings data
    """
    
    #Calculatate the overall winnings
    gw_data = gw_data[(gw_data.Gameweek < st.session_state['gw_id']) | (gw_data.Gameweek == st.session_state['gw_id'] & st.session_state['gw_status'])]
    mn_data = mn_data[mn_data.Month.isin(st.session_state['completed_months'])]

    gw_data_rankers = gw_data[gw_data['Rank'] == 1].groupby(['Gameweek', 'Rank']).size().reset_index(name='Count').sort_values('Gameweek')
    mn_data_rankers = mn_data[mn_data['Rank'] == 1].groupby(['Month', 'Rank']).size().reset_index(name='Count')

    merged_gw_df = gw_data.merge(gw_data_rankers, on=['Gameweek','Rank'], how='left', suffixes=('', '_rankers'))
    merged_mn_df = mn_data.merge(mn_data_rankers, on=['Month','Rank'], how='left', suffixes=('', '_rankers'))

    merged_gw_df['Total'] = 300 / merged_gw_df['Count']
    merged_mn_df['Total'] = 530 / merged_mn_df['Count']

    merged_gw_df.Total.fillna(0, inplace=True)
    merged_mn_df.Total.fillna(0, inplace=True)

    
    return merged_gw_df, merged_mn_df
    
