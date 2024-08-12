import csv
from Utils import gameweek as gw
from monthly import *
import os
from overall import *


lg = league()

mid = ''
manager_history_url = f'{p.base_url}entry/'

players = lg.get_league_players()
league_name = lg.get_league_name().replace(' ', '_').replace('/', '_')

if not os.path.exists(f'./Overall_Result/{league_name}'):
    os.mkdir(f'./Overall_Result/{league_name}')
if not os.path.exists(f'./Gameweek_Results/{league_name}'):
    os.mkdir(f'./Gameweek_Results/{league_name}')
if not os.path.exists(f'./Monthly_Results/{league_name}'):
    os.mkdir(f'./Monthly_Results/{league_name}')

phases = gw.get_phases()

gw_status = get_recent_completed_gameweek()
gw = gw_status[0]  # 8
# print(gw)
print('\n')
s = 1

start, end = 0, 0

fields1 = ['Rank', 'Player', 'Points']

# name of csv file
filename1 = f"./Overall_Result/{league_name}/overall_rank.csv"

# writing to csv file
with open(filename1, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields1)

for key, value in phases.items():
    if value[0] <= gw <= value[1] and key != 'Overall':
        start, end = value[0], value[1]
        month = key
        break

session = requests.session()
msg = ''
msg_all = 'Gameweek Standings\n\n'

gw_rnk = {}

for g in range(gw, gw + 1):
    for player in players:
        x = session.get(manager_history_url + str(player[1]) + '/history/').json()
        # if x['current']['event'] == gw:
        for event in x['current']:
            if event['event'] == g:
                print(player[0].split(' ')[0].capitalize() + ' ' + player[0].split(' ')[1].capitalize() + '\n')
                print('Points - ' + str(event['points']))
                print('Transfer Cost - ' + str(event['event_transfers_cost']))
                print('Net Points - ' + str(event['points'] - event['event_transfers_cost']))
                gw_rnk[player[0]] = event['points'] - event['event_transfers_cost']
                print('---------------------------')
                msg_all = msg_all + 'Player: ' + player[0].split(' ')[0].capitalize() + ' ' + player[0].split(' ')[
                    1].capitalize() + '\n\n' + 'Points - ' + str(event['points']) + \
                          '\nTransfer Cost - ' + str(event['event_transfers_cost']) + \
                          '\nNet Points - ' + str(event['points'] - event['event_transfers_cost']) + '\n\n'

        # writing to csv file
        with open(filename1, 'a', newline='') as csvfile1:
            # creating a csv writer object
            csvwriter1 = csv.writer(csvfile1)

            # writing the data rows
            csvwriter1.writerow(player[3:] + player[0:1] + player[2:3])

        csvfile1.close()

    r = {key: rank for rank, key in enumerate(sorted(set(gw_rnk.values()), reverse=True), 1)}
    gw_rnk_final = {
        k: [k, v, r[v]] for k, v in gw_rnk.items()}
    gw_rnk_final = [list(x[1]) for x in sorted(gw_rnk_final.items(), key=lambda x: x[1][2])]

    for i in gw_rnk_final:
        i.append(gw)
    #print(gw_rnk_final)

    fields = ['Player', 'Points', 'Rank', 'Gameweek']

    # name of csv file
    #filename = "/Users/Himanshu/PyCharm_Projects/FPL/Gameweek_Results/gameweek_" + str(g) + "_rank.csv"
    filename = f"./Gameweek_Results/{league_name}/gameweek_" + str(g) + "_rank.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(gw_rnk_final)
        #csvwriter.writerow()

if not gw_status[1]:
    for player in players:
        if player[0] == gw_rnk_final[0][0] or '':
            x = session.get(manager_history_url + str(player[1]) + '/history/').json()
            for event in x['current']:
                if event['event'] == gw:
                    msg = '\n*Gameweek ' + str(gw) + ' not over yet*\n\n'
                    msg = msg + 'GW ' + str(gw) + ' Leader: ' + player[0].split(' ')[0].capitalize() + ' ' + \
                          player[0].split(' ')[1].capitalize() + '\n\n' + 'Points - ' + str(event['points']) \
                          + '\nTransfer Cost - ' + str(event['event_transfers_cost']) + '\nNet Points - ' \
                          + str(event['points'] - event['event_transfers_cost']) + '\n'
else:
    msg1 = '\n*Gameweek ' + str(gw) + ' over!*\n'
    print(msg1+'*GW ' + str(gw) + ' Winner(s):*\n')
    for player in players:
        for winner in gw_rnk_final:
            if winner[2] == 1 and winner[0].upper() == player[0].upper():
                x = session.get(manager_history_url + str(player[1]) + '/history/').json()
                for event in x['current']:
                    if event['event'] == gw:
                        msg = msg + player[0].split(' ')[0].capitalize() + ' ' + \
                            player[0].split(' ')[1].capitalize() + '\n\n' + 'Points - ' + str(event['points']) \
                            + '\nTransfer Cost - ' + str(event['event_transfers_cost']) + '\nNet Points - ' \
                            + str(event['points'] - event['event_transfers_cost']) + '\n\n'

print(msg)
print('---------------------------' + '\n')

get_monthly_results()
print('\n' + '---------------------------' + '\n')
print('*Overall Leaders*' + '\n')
overall_leader('Fantasy_Kings_2023_24')

# resp = input('Do you want to send whatsapp notification? (Y/N): ')
#
# if resp.lower() == 'y':
#     w.send_whatsapp_message(msg, 'DH1kOsVQhEyB0XVjkJpx61')
# w.send_whatsapp_message(msg_all, 'DH1kOsVQhEyB0XVjkJpx61')

