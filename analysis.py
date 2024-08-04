import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# use glob to get all the csv files
# in the folder
path = f'./Gameweek_Results/Fantasy_Kings_2023_24/'
csv_files = glob.glob(os.path.join(path, "*.csv"))
plyr = 'Shaishav Bhatt'

df1 = pd.DataFrame(columns=['Gameweek', 'Rank', 'Points'])

# loop over the list of csv files
for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)

    # print the location and filename
    # print('Location:', f)
    print('File Name:', f.split("\\")[-1])

    # print the content
    # print('Content:')
    # print(df['Player'].to_string(index=False))

    row_index = df.loc[df['Player'] == plyr]  # .index[0]
    # row_index1 = df.loc[df['Rank'] == 1.0]

    for i, r in row_index.iterrows():
        print(str(r['Gameweek']) + '-' + str(r['Rank']) + '-' + str(r['Points']))

        lst = []
        lst.append([str(r['Gameweek']), str(r['Rank']), str(r['Points'])])

        df1 = df1._append({'Gameweek': r['Gameweek'], 'Rank': r['Rank'], 'Points': r['Points']}, ignore_index=True)
        df1 = df1.sort_values(by=['Gameweek'])

#for ind in df1.index:
#    print(df1['Gameweek'][ind], df1['Rank'][ind], df1['Points'][ind])

gw = df1['Gameweek']
rank = df1['Rank']
pts = df1['Points']

fig, ax1 = plt.subplots()

ax1.plot(gw, rank, color='black', marker='o', linewidth=1, label='Rank', alpha=0.7)
ax1.set_xlabel('Gameweek')
ax1.set_ylabel('Rank', color='black')
ax1.tick_params(axis='y', labelcolor='black')
# ax1.gca().invert_yaxis()
ax1.set_ylim(0.5, 16)
ax1.invert_yaxis()

# Create a twin axis
ax2 = ax1.twinx()
p = ax2.bar(gw, pts, color='green', label='Points', alpha=0.5)
ax2.set_ylabel('Points', color='black')
ax2.tick_params(axis='y', labelcolor='black')
ax2.bar_label(p, label_type='center')

plt.title(f'Player Performance - {plyr}')
plt.grid = True

plt.show()
