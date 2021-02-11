

from functools import lru_cache
from pathlib import Path
import re
import string

import pandas as pd


# df = pd.DataFrame(data['players']['player'])


def defense_to_dst(col):
    """Changes position column Def --> DST"""
    return col.str.replace('Def', 'DST')


def fix_name(row, namecol='name_'):
    """Fixes player name to first last. Changes DST to Nickname Defense"""
    if row.position == 'DST':
        nickname, city = getattr(row, namecol).split(', ')
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

    # step one: drop unneded columns
    wanted = ['position', 'name', 'id', 'team', 'nfl_id']
    df = df.loc[:, wanted]

    # step two: fix positions
    df['position'] = df['position'].str.replace('Def', 'DST')

    # step three: fix names
    df['name_norm'] = df['name']
    df['name_norm'] = df.apply(fix_name, args=('name_norm',), axis=1)


class PlayerXref:
    @lru_cache(maxsize=None)
    def blitz_mfl_dict(self, df):
        """Creates dict of blitz_id: mfl_id"""
        return {k: v for k, v in zip(df['rg_player_id'], df['mfl_player_id'])}

    @lru_cache(maxsize=None)
    def load_blitz_mfl_xref(self):
        """Loads xref file for matching players
        
        Returns DataFrame with columns
        rg_player_id, rg_player_name, pos, team  
        mfl_player_id, mfl_player_name
        """
        fn = Path(__file__).parent / 'rg_mfl_xref.csv'
        return pd.read_csv(fn)

    def merge_blitz_ffa(self, blitzdf, ffadf):
        """Merges blitz and ffa projections. Use blitz as left join - has salaries"""
        d = self.mfl_blitz_dict(self.load_blitz_mfl_xref())
        ffadf['playerid'] = ffadf['id'].map(d)
        return d.join(ffadf, on='playerid', rsuffix='_ffa')

    @lru_cache(maxsize=None)
    def mfl_blitz_dict(self, df):
        """Creates dict of mfl_id: blitz_id"""
        return {k: v for k, v in zip(df['mfl_player_id'], df['rg_player_id'])}


if __name__ == '__main__':
    pass
