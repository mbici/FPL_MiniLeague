import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import re

numbers = re.compile(r'(\d+)')


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# use glob to get all the csv files
# in the folder
path = f'./Gameweek_Results/Fantasy_Kings_2023_24/'
csv_files = sorted(glob.glob(os.path.join(path, "*.csv")), key=numericalSort)
plyr = ['fawad dhundware', 'Abhishek Kenkre', 'harshal hariyar', 'Sunit Gupte', 'Karthik Devadiga', 'Vighnesh Rajan',
        'Rohan Menon', 'Himanshu Masani', 'suresh choudhary', 'Ajinkya Chitnis', 'vishal polkam', 'Nikhil Patil',
        'Kaustubh Patil', 'Arvind Ramkumar', 'Shaishav Bhatt', 'Sumit Uttekar']

df1 = pd.DataFrame(columns=['Gameweek', 'Player', 'Points', 'Rank'])

# loop over the list of csv files
for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)

    # print the location and filename
    # print('Location:', f)
    # print('File Name:', f.split("\\")[-1])

    # print the content
    # print('Content:')
    # print(df['Player'].to_string(index=False))

    for i in plyr:
        r = df.loc[df['Player'] == i]

        gw = r['Gameweek'].values[0]
        pl = r['Player'].values[0]
        pts = r['Points'].values[0]

        r1 = df1.loc[(df1['Player'] == i) & (df1['Gameweek'] == gw - 1)]
        pl_tot = r1['Points'].sum() + pts

        lst = [{'Gameweek': gw, 'Player': pl, 'Points': pl_tot, 'Rank': ''}]
        df1 = df1._append(lst, ignore_index=True)

    # print(df1)
    # print(df1.loc[df1['Gameweek'] == gw])
    df1.loc[df1['Gameweek'] == gw, 'Rank'] = df1.loc[df1['Gameweek'] == gw, 'Points'].rank(method='dense',
                                                                                           ascending=False)

p = 'vishal polkam'
p1 = 'Himanshu Masani'
cnt = 1

fig, ax1 = plt.subplots(1)

for p in ['vishal polkam', 'harshal hariyar', 'Himanshu Masani', 'Shaishav Bhatt', 'fawad dhundware']:
    df3 = df1.loc[(df1['Player'] == p)]
    pgw = df3['Gameweek']
    prank = df3['Rank']

    ax1.plot(pgw, prank, marker='o', label=p, linewidth=1, alpha=0.7, linestyle='dashdot')
    ax1.legend()

ax1.set_xlabel('Gameweek')
ax1.set_ylabel('Rank')
ax1.set_ylim(0.7, 16.2)
ax1.set_xlim(0.7, 38.2)
ax1.invert_yaxis()
ax1.set_title('Player Rank Trend')
plt.show()

# df2 = df1.loc[df1['Player']==p]
# df3 = df1.loc[df1['Player']==p1]
#
# #print(df2.head(100))
# pgw = df2['Gameweek']
# prank = df2['Rank']
#
# pgw1 = df3['Gameweek']
# prank1 = df3['Rank']
#
# fig, ax1 = plt.subplots(1)
#
# ax1.plot(pgw, prank, label='Vishal')
# ax1.plot(pgw1, prank1, label='Himanshu')
# ax1.legend()
#
# plt.show()

# plt.plot(pgw, prank, color='black', marker='o', linewidth=1, alpha=0.7)
# plt.xlabel('Gameweek')
# plt.xlabel('Rank', color='black')
# plt.tick_params(axis='y', labelcolor='black')
# plt.ylim(0.5, 16)
# plt.gca().invert_yaxis()
# plt.title(f'Player Rank Trend - {p}')
#
# plt.show()
