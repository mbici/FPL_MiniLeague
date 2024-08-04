import pandas as pd
import os

gw = []
win_df = pd.DataFrame(columns=['Name', 'Count'])

lst = os.listdir('./Gameweek_Results/Fantasy_Kings_2023_24/')
for i in lst:
    gw.append(int(i.split('_')[1]))
    gw_win_df = pd.read_csv(f'./Gameweek_Results/Fantasy_Kings_2023_24/{i}')
    #print(gw_win_df['Player'].loc[gw_win_df['Rank'] == 1].isin(win_df.Name).to_string(index=False))
    if gw_win_df['Player'].loc[gw_win_df['Rank'] == 1].isin(win_df.Name).to_string(index=False) == 'True':
        #print(win_df.Name)
        p = gw_win_df.index(gw_win_df['Player'].loc[gw_win_df['Rank'] == 1])
        print(p)
        win_df['Count'].loc[win_df['Name'] == gw_win_df['Player'].loc[gw_win_df['Rank'] == 1]] = win_df['Count'] + 1
        print(win_df)
    else:
        x = gw_win_df['Player'].loc[gw_win_df['Rank'] == 1].to_string(index=False)
        df2 = pd.DataFrame({'Name': [x], 'Count': [1]})
        win_df = pd.concat([win_df, df2], ignore_index=True)
        print(win_df)
print(win_df.to_string(index=False))

# print(sorted(gw))



#win_df = pd.DataFrame(players, columns=['Name', ''])