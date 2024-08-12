import requests
from Params import params as p
import logging
import pandas as pd

logging.basicConfig(level=logging.WARNING)


class league:
    def __init__(self, leagueId=140708):
        self.leagueId = leagueId
        self.base_url = p.base_url

    def conn(self):
        """
        Function to get mini league data using fpl api in json format
        :return: Json data for the mini league
        """

        connect = {}
        session = requests.session()
        league_url = f'{self.base_url}leagues-classic/{self.leagueId}/standings'  # 288563,331953,140708

        try:
            connect = session.get(league_url).json()
            logging.info('Mini league connection successful')

        except Exception as e:
            print(e)
            print('Could not connect to the league url')

        return connect

    def get_league_name(self):
        """
        Function to get league name
        :return: String of League Name
        """

        data = self.conn()
        league_name = data['league']['name']
        logging.info('League Name is -> ' + str(league_name))

        return league_name

    def get_league_players(self):
        """
        Function to get player details
        :return: List of players from the mini league
        """

        data = self.conn()
        players = []

        try:
            players = [{'Id': player['entry'], 'Team': player['entry_name'],
                        'Player': player['player_first_name'].capitalize() + ' ' + player[
                            'player_last_name'].capitalize()}
                       for player in data['new_entries']['results']]
            logging.info('Total Players in the league -> ' + str(len(players)))

        except Exception as e:
            print(e)

        return players

    def get_league_standings(self):
        """
        Function to get mini league standings
        :return: List of players with latest standings
        """

        data = self.conn()
        standings = []

        try:
            standings = [{player['entry']: {'total': player['total'], 'rank': player['rank_sort']}}
                         for player in data['standings']['results']]

        except Exception as e:
            print(e)

        return standings


if __name__ == '__main__':
    t = league(140708)

    print(t.get_league_name())
    print('------------------------------------------------')
    p_df = pd.DataFrame.from_records(t.get_league_players())
    print(t.get_league_players())
    p_df.rename(columns={'id': 'Player Id', 'team': 'Team Name', 'player': 'Player Name'})
    print(p_df.get('Player'))  # p_df.to_string(index=False)
    print('------------------------------------------------')
    print(t.get_league_standings())
