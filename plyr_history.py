from league import *
from Params import params as p
from datetime import datetime, timedelta
import requests
import pandas as pd

logging.basicConfig(level=logging.WARNING)


def plyr_hist(pl=None):
    try:
        session = requests.session()
        data = session.get(f'{p.base_url}entry/{pl}/history/').json()

        hist = [{'Season':x['season_name'], 'Rank':x['rank']} for x in data['past']]
        df = pd.DataFrame(hist)
        logging.info('API access successful!!')

    except Exception as e:
        print('No player id provided')
        hist = None

    return df


if __name__ == '__main__':
    print(plyr_hist(777321))
