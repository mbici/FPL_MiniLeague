import pandas as pd
import csv
import os
import sys
# from trend import numericalSort as n
import glob

weekly_dir = './Gameweek_Results/Fantasy_Kings_2023_24/'
monthly_dir = './Monthly_Results/Fantasy_Kings_2023_24/'
overall_dir = './Overall_Result/Fantasy_Kings_2023_24/'

m_df = pd.DataFrame(columns=['Month', 'Player', 'Points', 'Rank'])
w_df = pd.DataFrame(columns=['Gameweek', 'Player', 'Points', 'Rank'])


def monthly_stat():
    global m_df
    csv_files = sorted(glob.glob(os.path.join(monthly_dir, "*.csv")))
    for filename in csv_files:
        if filename.split('/')[3].split('_')[1].split('.')[0] != 'June':
            df = pd.read_csv(filename)
            rr = df.loc[df['Rank'] == 1]
            for i, r, in rr.iterrows():
                lst = [{'Month': filename.split('/')[3].split('_')[1].split('.')[0], 'Player': r['Name'],
                        'Points': r['Points'], 'Rank': r['Rank']}]
                m_df = m_df._append(lst, ignore_index=True)

    x = m_df.groupby(['Player'])['Rank'].count()
    sortedDF = x.sort_values(ascending=False)
    print('Monthly Awards: \n')
    return sortedDF


def weekly_stat():
    global w_df
    csv_files = sorted(glob.glob(os.path.join(weekly_dir, "*.csv")))
    for filename in csv_files:
        # if filename.split('/')[3].split('_')[1].split('.')[0] != 'March':
        df = pd.read_csv(filename)
        rr = df.loc[df['Rank'] == 1]
        for i, r in rr.iterrows():
            p = r['Player'].split(' ')[0].capitalize() + ' ' + r['Player'].split(' ')[1].capitalize()
            lst = [{'Gameweek': r['Gameweek'], 'Player': p,
                    'Points': r['Points'], 'Rank': r['Rank']}]
            w_df = w_df._append(lst, ignore_index=True)

    x = w_df.groupby(['Player'])['Rank'].count()
    sortedDF = x.sort_values(ascending=False)

    print('\n----------------------\n\nWeekly Awards: \n')
    return sortedDF


if __name__ == "__main__":
    print(monthly_stat().to_string())
    print(weekly_stat())
