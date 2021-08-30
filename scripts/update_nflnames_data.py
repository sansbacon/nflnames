from pathlib import Path
import re
import string

import requests
import pandas as pd


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


# df = pd.DataFrame(data['players']['player'])


def defense_to_dst(col):
    """Changes position column Def --> DST"""
    return col.str.replace('Def', 'DST')


def fix_name(row, namecol='mfl_name'):
    """Fixes player name to first last. Changes DST to Nickname Defense"""
    if row.position == 'DST':
        nickname, _ = getattr(row, namecol).split(', ')
        return f'{normalize_name(nickname)} defense'
    parts = getattr(row, namecol).split(', ')
    first = normalize_name(parts[1])
    last = normalize_name(parts[0])
    return f'{first} {last}'


def normalize_name(s):
    """Strips suffix and extra characters to create lowercase name"""
    try:
        news = s.replace('Jr.', '').replace('Sr.', '').replace('III', '').replace('II', '').strip()
        news = ''.join([c for c in news if c not in string.punctuation])
        news = re.sub(r'\s+(?:IV|V)\b', '', news)
        return re.sub(r'\s+', ' ', news).lower()
    except AttributeError:
        return s


def clean_mfl_players(df):
    """Parses MFL players resources into players dataframe"""

    # fix positions
    df['position'] = df['position'].str.replace('Def', 'DST').str.replace('PK', 'K')
    wanted_positions = {'DST', 'QB', 'RB', 'WR', 'TE', 'K'}
    df = df.loc[df.position.isin(wanted_positions), :]

    # fix names
    remap = {
        'id': 'mfl_id',
        'name': 'mfl_name',
        'position': 'pos',
    }
    df = df.rename(columns=remap)
    df = df.assign(name_norm=df.apply(fix_name, axis=1)

    # drop unneded columns
    wanted = ['id', 'name', 'name_norm', 'position', 'team']
    df = df.loc[:, wanted]

    return df.rename(columns=remap)

