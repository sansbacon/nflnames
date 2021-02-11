import requests


def download_mfl_players(since=''):

    """Downloads MFL players resource"""
    params = {
      'TYPE': 'players',
      'L': '',
      'APIKEY': '',
      'DETAILS': 1,
      'SINCE': since,
      'PLAYERS': '',
      'JSON': 1
    }
    url = 'https://api.myfantasyleague.com/2020/export?'
    return requests.get(url, params).json()
