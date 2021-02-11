# players.py
from functools import lru_cache


def mfl_players(since=''):

    """Gets MFL players list"""
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
    mflp = requests.get(url, params).json()
    return pd.DataFrame(mflp['players']['player'])

   

def normalize_name(s):
    """Strips suffix and extra characters to create lowercase name"""
    news = s.replace('Jr.', '').replace('Sr.', '').replace('III', '').replace('II', '').strip()
    news = ''.join([c for c in news if c not in string.punctuation])
    return news.lower()


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
