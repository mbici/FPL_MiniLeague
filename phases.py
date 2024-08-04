from datetime import datetime
import requests
import json
from gameweek import get_recent_completed_gameweek


def get_phases():
    """
    List all the phases
    :return: Dictionary of Months and GW Start/Stop numbers
    """

    data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    data = json.loads(data.content)

    phases = data['phases']
    gw = {}

    for phase in phases:
        gw[phase['name']] = [phase['start_event']] + [phase['stop_event']]

    return gw


def get_till_latest_phase():
    """
    Get the latest and completed phase's month name
    :return: list of month values
    """
    phase = get_phases()
    keys = phase.keys()
    gw = get_recent_completed_gameweek()
    # l = [y for y in keys if gw is not None and gw >= phase[y][0] and gw >= phase[y][1] and y != 'Overall']
    # k = []
    #
    # for y in keys:
    #     if phase[y][0] < gw < phase[y][1] and y != 'Overall':
    #         k.append(y + '-In Progress')
    #     elif gw >= phase[y][1] and y != 'Overall':
    #         k.append(y)
    # print(k)
    #return l
    for (k, v) in phase.items():
        if gw[0]>=v[0] and gw[0]<=v[1] and k != 'Overall':
            return k, v


if __name__ == '__main__':
    print(get_phases())
    print(get_till_latest_phase())
