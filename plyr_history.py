from Utils.league import *
from Params import params as p
import requests
import pandas as pd

logging.basicConfig(level=logging.WARNING)


def plyr_hist(pl=None, plyrLink=None):
    """
    Function to return the historical season data for managers
    :param pl: player id from FPL
    :param plyrLink: dictionary of player id and player name
    :return: dataframe of historical ranks for all managers in Fantasy Kings
    """

    df = pd.DataFrame(columns=['Season', 'Rank', 'PlayerId', 'Player Name'])
    try:
        for i in pl:
            session = requests.session()
            data = session.get(f'{p.base_url}entry/{i}/history/').json()

            hist = [{'Season': x['season_name'], 'Rank': x['rank'], 'PlayerId': i} for x in data['past']]
            df1 = pd.DataFrame(hist)
            for j in plyrLink:
                for k, v in j.items():
                    if v == i:
                        df1['Player Name'] = k
                        break
            df = pd.concat([df, df1])
            logging.info('API access successful!!')

    except Exception as e:
        print('No player id provided')
        hist = None

    return df


if __name__ == '__main__':
    print(plyr_hist([777321,1631933]))
