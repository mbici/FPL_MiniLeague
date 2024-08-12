from Utils.league import *
from Utils.gameweek import *
from phases import *
import requests
import pandas as pd
import Params as p

lg = league()


def get_monthly_results():
    gw_status = get_recent_completed_gameweek()
    gw = gw_status[0]
    m = get_till_latest_phase()

    players = lg.get_league_players()

    league_name = lg.get_league_name().replace(' ', '_').replace('/', '_')

    monthValue = m[0]
    mStart = m[1][0]
    mEnd = m[1][1]

    df = pd.DataFrame(players, columns=['Name', 'Player Id', 'Points', 'Rank'])
    df.drop(columns=['Points', 'Rank'], inplace=True)
    df['Points'] = [''] * len(players)
    df['Rank'] = [''] * len(players)

    manager_history_url = f'{p.base_url}entry/'

    session = requests.session()

    for player in players:
        pts = 0
        x = session.get(manager_history_url + str(player[1]) + '/history/').json()
        for event in x['current']:
            if mStart <= event['event'] <= mEnd:
                pts = pts + event['points'] - event['event_transfers_cost']
        # locate the row to update
        row_index = df.loc[df['Player Id'] == player[1]].index[0]
        # update the row with new values
        df.loc[row_index, 'Points'] = pts
        df.loc[row_index, 'Name'] = player[0].split(' ')[0].capitalize() + ' ' + player[0].split(' ')[1].capitalize()

    df['Rank'] = df['Points'].rank(method='dense', ascending=False)
    df.sort_values(by=['Rank'], ascending=True, inplace=True)
    # print(df)

    df.to_csv(f'./Monthly_Results/{league_name}/Month_' + monthValue + '.csv', index=False)

    row_index = df.loc[df['Rank'].isin([1.0, 2.0, 3.0, 4.0, 5.0])]  # .index[0]
    row_index1 = df.loc[df['Rank'] == 1.0]

    if gw == mEnd and gw_status[1]:
        print('*Monthly Winner(s) - ' + monthValue + ':*\n')
        for i, r in row_index1.iterrows():
            print(r['Name'])
            print('Points - ' + str(r['Points']) + '\n')
            # print(i[1][0])
            # print('Points - ' + str(i[1][2]) + '\n')
    elif mStart <= gw <= mEnd:  # and not gw_status[1]::
        print('*Monthly Leaders - ' + monthValue + '*\n')
        for i, r in row_index.iterrows():
            # print(df.loc[row_index, 'Name'] + '\n')
            # print('Points - ' + str(df.loc[row_index, 'Points']))
            print(str(r['Rank']).replace('.0', '') + '. ' + r['Name'] + ' - ' + str(r['Points']))
            # print('Points - ' + str(r['Points']) + '\n')


if __name__ == "__main__":
    get_monthly_results()
