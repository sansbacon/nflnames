from pathlib import Path

import numpy as np
import pandas as pd
import requests

from nflnames import *


DATADIR = Path(__file__).parent.parent / 'nflnames' / 'data'


# get the data
url = 'https://api.myfantasyleague.com/2020/export?TYPE=players&L=&APIKEY=&DETAILS=1&SINCE=&PLAYERS=&JSON=1'
r = requests.get(url)
data = r.json()

df = pd.DataFrame(data['players']['player'])

# standardize and filter positions
df = df.assign(position=df.position.apply(standardize_positions))
positions = ['DST', 'RB', 'TE', 'WR', 'PK', 'QB']
df = df.loc[df.position.isin(positions), :]

# standardize team codes
df['team'] = df['team'].apply(standardize_team_code)

# standardize names
df['first_last'] = df['name'].apply(rearrange_name)
df.loc[df.position == 'DST', 'standard_name'] = df.loc[df.position == 'DST', 'first_last'].apply(standardize_team_name)
df['standard_name'] = np.where(df.position == 'DST', df.first_last.apply(standardize_defense_name), df.first_last.apply(standardize_player_name))

# filter unneeded columns
wanted = ['id', 'name', 'first_last', 'standard_name', 'position', 'team', 'draft_year', 'college',
          'stats_id', 'sportsdata_id', 'espn_id', 'cbs_id', 'nfl_id']
df = df.loc[:, wanted]

# rename columns
remap = {
  'id': 'mfl_id',
  'name': 'mfl_name',
  'position': 'pos',
}

df = df.rename(columns=remap)

# write to disk
df.to_csv('/home/sansbacon/workspace/nflnames/nflnames/data/master_players.csv', index=False)