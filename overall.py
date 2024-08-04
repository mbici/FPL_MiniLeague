import pandas as pd


def overall_leader(lname):
    df = pd.read_csv(f'./Overall_Result/{lname}/overall_rank.csv')
    row_index = df.loc[df['Rank'].isin([1, 2, 3])]

    for i, r in row_index.iterrows():
        print(str(r['Rank']) + '. ' + r['Player'].split(' ')[0].capitalize() + ' ' +
              r['Player'].split(' ')[1].capitalize() + ' - ' + str(r['Points']))


def update_gw(lname):
    for i in range(1, 2):
        df = pd.read_csv(f'./Gameweek_Results/{lname}/gameweek_{i}_rank.csv')
        df['Gameweek'] = i
        df.to_csv(f'./Gameweek_Results/{lname}/gameweek_{i}_rank.csv')


def del_col(lname):
    for i in range(1, 28):
        df = pd.read_csv(f'./Gameweek_Results/{lname}/gameweek_{i}_rank.csv', index_col=False)
        df.drop(df.columns[[0, 1]], axis=1, inplace=True)
        df.to_csv(f'./Gameweek_Results/{lname}/gameweek_{i}_rank.csv', index=False)


if __name__ == "__main__":
    # del_col('Fantasy_Kings_2023_24')
    overall_leader('Fantasy_Kings_2023_24')
