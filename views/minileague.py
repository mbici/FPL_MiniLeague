import pandas as pd
import streamlit as st
import Utils.gsheet_conn as gs
import Utils.gameweek as gwk
from Utils.league import *
from fpl_streamlit_app import deadline, latest_gw, completed_months
import Utils.standings as stg

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

if 'gw_status' not in st.session_state:
    st.session_state['latest_gw'] = latest_gw[0]
    st.session_state['gw_status'] = latest_gw[1]
    st.session_state['completed_months'] = completed_months

gw_winnings = mn_winnings = 0.0
# Refresh data from Google Sheets
ovr_data, gw_data, mn_data =  stg.data_refresh()

# Calculate winnings data for Gameweek and Monthly
gw_winning_df, mn_winnings_df = stg.winnings_data(gw_data, mn_data)
gw_wins_agg = gw_winning_df.groupby('Player')['Total'].sum().reset_index()
mn_wins_agg = mn_winnings_df.groupby('Player')['Total'].sum().reset_index()

    # ovr_data.loc[0, ['Rank']] = '🥇'
    # ovr_data.loc[1, ['Rank']] = '🥈'
    # ovr_data.loc[2, ['Rank']] = '🥉'
    # ovr_data.loc[3, ['Rank']] = '🏅'

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


def render_grid(df: pd.DataFrame, column_order: list | None = None, height: int = 780) -> str:
    """
    Render a pandas DataFrame as a visually appealing HTML grid with soothing colors.
    Rows where Rank == 1 will be enlarged and highlighted.
    """
    # Determine columns to show
    cols = column_order if column_order is not None else list(df.columns)

    # CSS for the grid
    grid_css = '''
    <style>
    .fpl-grid { align-items:left; display:block; width:100%; max-height: __HEIGHT__px; overflow:auto; padding:8px; box-sizing:border-box; }
    .fpl-grid .header, .fpl-grid .row { align-items:left;  display:grid; grid-template-columns: 80px 1fr 120px 120px 120px; gap:10px; padding:2px 4px; border-radius:10px; }
    .fpl-grid .header { position:sticky; top:0; background: linear-gradient(90deg, rgba(50,120,60,0.95), rgba(50,200,110,0.95)); color:#f3c911; font-weight:700; z-index:5; box-shadow:0 4px 12px rgba(12,70,20,0.08);text-align:left;}    
    .fpl-grid .header .cell { font-size: 1.48rem; color:#ffffe0; padding:10px 4px;}
    .fpl-grid .row { background: linear-gradient(180deg, rgba(250,250,248,0.9), rgba(240,248,240,0.9)); margin:8px 0; transition:transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;}
    .fpl-grid .row:hover { transform: translateY(-4px); box-shadow: 0 10px 28px rgba(18,58,18,0.06);}    
    .fpl-grid .cell { padding:6px 4px; color:#0b2b14; font-size:1.02rem; text-align:left; }
    .fpl-grid .player { text-align:left; font-weight:500; font-size:1.02rem; }
    .fpl-grid .rank { text-align:left; font-weight:500; color:#0b3620; font-size:1.02rem; }
    .fpl-grid .points { text-align:left; font-weight:500; color:#1a3e20; font-size:1.02rem; }
    .fpl-grid .transfer, .fpl-grid .gross { text-align:left; font-weight:500; font-size:1.02rem; }
    .fpl-grid .winnings, { text-align:center; font-weight:500; font-size:1.02rem; }

    /* highlighted (top) row styling */
    .fpl-grid .row.highlight { text-align:left; transform: scale(1.05); background: linear-gradient(90deg, #f3c901, #f3c901); box-shadow: 0 18px 46px rgba(33,150,83,0.12); }
    .fpl-grid .row.highlight .player { font-weight:800;font-size:1.48rem; text-align:center;}
    .fpl-grid .row.highlight .rank { font-weight:800;font-size:1.48rem; text-align:right;}
    .fpl-grid .row.highlight .gross { font-weight:800;font-size:1.48rem; text-align:left;}
    .fpl-grid .row.highlight .transfer { font-weight:800;font-size:1.48rem; text-align:left;}
    .fpl-grid .row.highlight .points { font-weight:800;font-size:1.48rem; text-align:left;}

    /* responsive fallback for narrow screens */
    @media (max-width:720px) {
        .fpl-grid .header, .fpl-grid .row { grid-template-columns: 60px 1fr 80px; }
        .fpl-grid .gross, .fpl-grid .transfer { display:none; }
    }
    </style>
    '''.replace('__HEIGHT__', str(height))

    # Build header and rows
    header_cells = ''.join([f"<div class='cell'>{c}</div>" for c in cols])
    rows_html = ''
    for _, r in df.iterrows():
        cls = 'row'
        try:
            if int(r.get('Rank', 0)) == 1:
                cls = 'row highlight'
        except Exception:
            pass

        cell_html = ''
        for c in cols:
            value = r.get(c, '')
            cell_class = 'cell'
            if str(c).lower() == 'player':
                cell_class += ' player'
            if str(c).lower() == 'rank':
                cell_class += ' rank'
            if str(c).lower() == 'points':
                cell_class += ' points'
            if str(c).lower() == 'transfer':
                cell_class += ' transfer'
            if str(c).lower() == 'gross':
                cell_class += ' gross'
            if str(c).lower() == 'winnings':
                cell_class += ' winnings'

            cell_html += f"<div class='{cell_class}'>{'' if pd.isna(value) else value}</div>"

        rows_html += f"<div class='{cls}'>{cell_html}</div>"

    html = f"""
    {grid_css}
    <div class='fpl-grid' role='table'>
      <div class='header'>{header_cells}</div>
      {rows_html}
    </div>
    """
    return html


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
        person = ovr_data.iloc[selection]['Player'].to_string(index=False).split(' ')
        personC = person[0].capitalize() + ' ' + person[1].capitalize()

        # In case the selection is None then a static text to be displayed above the widgets section else selected name
        if len(selection) > 0:
            playerSelected = personC
            gw_winnings = gw_winning_df.loc[gw_winning_df['Player'] == personC, 'Total'].sum()
            mn_winnings = mn_winnings_df.loc[mn_winnings_df['Player'] == personC, 'Total'].sum()
        else:
            playerSelected = '***Select a player***'


    # Metric Widgets section
    with mc:
        st.markdown(1 * "<br />", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: white;'>{playerSelected}</h4>", unsafe_allow_html=True)
        st.subheader('', anchor=False, divider='rainbow')
        st.markdown(1 * "<br />", unsafe_allow_html=True)

        # if gw_winnings is not None:
        st.markdown(f"""
                    <style>
                    {css}
                    </style>
                    """, unsafe_allow_html=True)

        g, m = st.columns(2)
        with g:
            st.metric('Weekly Winnings', '₹ ' + max(str(gw_winnings),'0'))

        with m:
            st.metric('Monthly Winnings', '₹ ' + max(str(mn_winnings),'0'))

        st.markdown(2 * "<br />", unsafe_allow_html=True)

        st.metric('Rank', {len(selection) > 0: ovr_data.loc[ovr_data['Player'] == personC, 'Rank']
                    .to_string(index=False)}.get(True),
                    delta=int({len(selection) > 0: ovr_data.loc[ovr_data['Player'] == personC, 'Last_Rank']
                    .to_string(index=False)}.get(True, 0)) -
                            int({len(selection) > 0: ovr_data.loc[ovr_data['Player'] == personC, 'Rank']
                    .to_string(index=False)}.get(True, 0)),
                    delta_color='normal')

    st.write('\n'*3)
    # st.write('\n')
    # st.write('\n')    

with tab_gw:
    # Gameweek Ranking Table section
    st.subheader('Gameweek Ranking', anchor=False)
    option = st.slider("Select Gameweek", 1, 38, latest_gw[0], label_visibility='collapsed')
    gw_data_option = gw_data.loc[gw_data['Gameweek'] == option].sort_values(by=['Rank'])
    st.write('\n')
    st.write('\n')

    if gw_data_option.empty:
        st.write('No data available for the selected gameweek.')
    else:
        # Render a custom HTML/CSS grid for a more pleasing visual
        html = render_grid(gw_data_option[['Rank', 'Player', 'Gross', 'Transfer', 'Points']],
                           column_order=['Rank', 'Player', 'Gross', 'Transfer', 'Points'],
                           height=780)
        st.markdown(html, unsafe_allow_html=True)

# Monthly Ranking Table section
with tab_mn:
    ongoing_month = gwk.get_ongoing_month()
    st.subheader('Monthly Ranking', anchor=False)
    option1 = st.select_slider("Select Month", label_visibility='collapsed',
                                options=['August', 'September', 'October', 'November', 'December', 'January',
                                        'February', 'March', 'April', 'May'],
                                value=ongoing_month if ongoing_month else 'August')

    mn_data_option = mn_data.loc[mn_data['Month'] == option1].sort_values(by=['Rank'])
    # mn_data_option.iloc[0, 2] = '🏆'
    st.write('\n')
    st.write('\n')
    if mn_data_option.empty:
        st.write('No data available for the selected month.')
    else:
        html = render_grid(mn_data_option[['Rank', 'Player', 'Points']],
                           column_order=['Rank', 'Player', 'Points'],
                           height=780)
        st.markdown(html, unsafe_allow_html=True)

# Winnings Table section
wins_agg_final = pd.merge(gw_wins_agg, mn_wins_agg, on='Player', how='outer', suffixes=('_GW', '_MN'))
wins_agg_final['Winnings'] = wins_agg_final['Total_GW'].fillna(0) + wins_agg_final['Total_MN'].fillna(0)
wins_agg_final = wins_agg_final[['Player', 'Winnings']].sort_values(by='Winnings', ascending=False).reset_index(drop=True)
wins_agg_final['#'] = wins_agg_final.index + 1

first_four = ovr_data['Player'].iloc[:4].astype(str).str.strip().tolist()
prizes = [7200, 4500, 3100, 1500]
prize_map = dict(zip(first_four, prizes))

# Consider the overall winnings in calculation only during and after gameweek 38
if latest_gw[0] == 38 and latest_gw[1]:
    # update existing winners
    for player, prize in prize_map.items():
        mask = wins_agg_final['Player'].astype(str).str.strip() == player
        if mask.any():
            wins_agg_final.loc[mask, 'Winnings'] = wins_agg_final.loc[mask, 'Winnings'] + prize

    # re-sort and reset index after applying prizes
    wins_agg_final = wins_agg_final.sort_values(by='Winnings', ascending=False).reset_index(drop=True)

with tab_winnings:
    st.subheader('Total Winnings', anchor=False)
    if len(wins_agg_final) == 0:
        st.write('No winnings data available yet.')
    else:
        # st.dataframe(wins_agg_final, hide_index=True, column_order=['Player', 'Winnings'], height=780,
        #             column_config={'Player': st.column_config.Column(width='medium'),
        #                         'Winnings': st.column_config.Column(width='small')})
        html = render_grid(wins_agg_final[['#', 'Player', 'Winnings']],
                           column_order=['#', 'Player', 'Winnings'],
                           height=780)
        st.markdown(html, unsafe_allow_html=True)
