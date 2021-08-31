# nflnames/nflnames/teams.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

"""
Converts various team name formats to standard format
Different sites use different names for the same NFL teams

Examples:

teams = ['JAX', 'kcc', 'gbp']
>>>is_standardized(teams)
False

>>>standardize_team_codes(teams)
['JAC', 'KC', 'GB']

"""
import logging
from typing import Dict, List, Set, Tuple

logging.getLogger(__file__).addHandler(logging.NullHandler())


TEAM_CODES = {
  'ARI': ['ari', 'ARZ', 'CRD', 'Arizona Cardinals', 'Cardinals', 'Arizona', 'crd'],
  'ATL': ['FAL', 'Atlanta Falcons', 'Falcons', 'Atlanta', 'atl'],
  'BAL': ['RAV', 'Baltimore Ravens', 'Ravens', 'Baltimore', 'rav'],
  'BUF': ['BIL', 'Buffalo Bills', 'Bills', 'Buffalo', 'buf'],
  'CAR': ['Carolina Panthers', 'Panthers', 'Carolina', 'car'],
  'CHI': ['Chicago Bears', 'Bears', 'Chicago', 'chi'],
  'CIN': ['CIN', 'Cincinnati Bengals', 'Bengals', 'Cincinnati', 'cin'],
  'CLE': ['CLE', 'Cleveland Browns', 'Browns', 'Cleveland', 'cle'],
  'DAL': ['DAL', 'Dallas Cowboys', 'Cowboys', 'Dallas', 'dal'],
  'DEN': ['DEN', 'Denver Broncos', 'Broncos', 'Denver', 'den'],
  'DET': ['DET', 'Detroit Lions', 'Lions', 'Detroit', 'det'],
  'GB': ['GBP', 'Green Bay Packers', 'Packers', 'Green Bay', 'GNB', 'gnb'],
  'HOU': ['HOU', 'Houston Texans', 'Texans', 'Houston', 'htx'],
  'IND': ['IND', 'Indianapolis Colts', 'Colts', 'Indianapolis', 'clt'],
  'JAC': ['JAX', 'Jacksonville Jaguars', 'Jaguars', 'Jacksonville', 'jac', 'jax'],
  'KC': ['KCC', 'Kansas City Chiefs', 'Chiefs', 'Kansas City', 'kan', 'KAN'],
  'LAC': ['LAC', 'Los Angeles Chargers', 'LA Chargers', 'San Diego Chargers', 'Chargers', 'San Diego', 'SD', 'sdg', 'SDG'],
  'LAR': ['LAR', 'LA', 'Los Angeles Rams', 'LA Rams', 'St. Louis Rams', 'Rams', 'St. Louis', 'ram'],
  'LVR': ['OAK', 'Oakland Raiders', 'Raiders', 'Oakland', 'rai', 'Las Vegas', 'LV', 'Vegas', 'lvr', 'lv', 'vegas'],
  'MIA': ['MIA', 'Miami Dolphins', 'Dolphins', 'Miami', 'mia'],
  'MIN': ['MIN', 'Minnesota Vikings', 'Vikings', 'Minnesota', 'min'],
  'NE': ['NEP', 'New England Patriots', 'Patriots', 'New England', 'nwe', 'NWE'],
  'NO': ['NOS', 'New Orleans Saints', 'Saints', 'New Orleans', 'nor', 'NOR'],
  'NYG': ['New York Giants', 'Giants', 'nyg'],
  'NYJ': ['New York Jets', 'Jets', 'nyj'],
  'PHI': ['Philadelphia Eagles', 'Eagles', 'Philadelphia', 'phi'],
  'PIT': ['PBG', 'PIT', 'Pittsburgh Steelers', 'Steelers', 'Pittsburgh', 'pit'],
  'SF': ['SFX', 'San Francisco 49ers', '49ers', 'SFO', 'San Francisco', 'sfo'],
  'SEA': ['Seattle Seahawks', 'Seahawks', 'Seattle', 'sea'],
  'TB': ['TBB', 'Tampa Bay Buccaneers', 'Buccaneers', 'TBO', 'tam', 'TAM', 'Tampa', 'Tampa Bay'],
  'TEN': ['TIT', 'Tennessee Titans', 'Titans', 'Tennessee', 'oti', 'ten'],
  'WAS': ['WFT', 'Washington Redskins', 'Redskins', 'Washington', 'was', 'Football Team', 'Washington Football Team'],
  'FA': ['FA', 'Free Agent', 'UNK', 'Unknown'],
}


TEAM_NAMES = {
  'Arizona Cardinals': ['ARI', 'Cardinals', 'Arizona', 'crd'],
  'Atlanta Falcons': ['ATL', 'Falcons', 'Atlanta', 'atl'],
  'Baltimore Ravens': ['BAL', 'Ravens', 'Baltimore', 'rav'],
  'Buffalo Bills': ['BUF', 'Bills', 'Buffalo', 'buf'],
  'Carolina Panthers': ['CAR', 'Panthers', 'Carolina', 'car'],
  'Chicago Bears': ['CHI', 'Bears', 'Chicago', 'chi'],
  'Cincinnati Bengals': ['CIN', 'Bengals', 'Cincinnati', 'cin'],
  'Cleveland Browns': ['CLE', 'Browns', 'Cleveland', 'cle'],
  'Dallas Cowboys': ['DAL', 'Cowboys', 'Dallas', 'dal'],
  'Denver Broncos': ['DEN', 'Broncos', 'Denver', 'den'],
  'Detroit Lions': ['DET', 'Lions', 'Detroit', 'det'],
  'Green Bay Packers': ['GB', 'Packers', 'Green Bay', 'GNB', 'gnb'],
  'Houston Texans': ['HOU', 'Texans', 'Houston', 'htx'],
  'Indianapolis Colts': ['IND', 'Colts', 'Indianapolis', 'clt'],
  'Jacksonville Jaguars': ['JAC', 'JAX', 'Jaguars', 'Jacksonville', 'jac', 'jax'],
  'Kansas City Chiefs': ['KC', 'Chiefs', 'Kansas City', 'kan', 'KAN'],
  'Los Angeles Chargers': ['LAC', 'SDC', 'LA Chargers', 'San Diego Chargers', 'Chargers', 'San Diego', 'SD', 'sdg', 'SDG'],
  'Los Angeles Rams': ['LAR', 'Los Angeles Rams', 'LA Rams', 'St. Louis Rams', 'Rams', 'St. Louis', 'ram', 'STL'],
  'Las Vegas Raiders': ['LVR', 'OAK', 'Raiders', 'Oakland', 'rai', 'Las Vegas', 'LV', 'Vegas', 'lvr', 'lv', 'vegas'],
  'Miami Dolphins': ['MIA', 'Dolphins', 'Miami', 'mia'],
  'Minnesota Vikings': ['MIN', 'Vikings', 'Minnesota', 'min'],
  'New England Patriots': ['NE', 'Patriots', 'New England', 'NEP', 'nwe', 'NWE'],
  'New Orleans Saints': ['NO', 'Saints', 'New Orleans', 'NOS', 'nor', 'NOR'],
  'New York Giants': ['NYG', 'Giants', 'nyg'],
  'New York Jets': ['NYJ', 'Jets', 'nyj'],
  'Philadelphia Eagles': ['PHI', 'Eagles', 'Philadelphia', 'phi'],
  'Pittsburgh Steelers': ['PIT', 'Steelers', 'Pittsburgh', 'pit'],
  'San Francisco 49ers': ['SF', '49ers', 'SFO', 'San Francisco', 'sfo'],
  'Seattle Seahawks': ['SEA', 'Seahawks', 'Seattle', 'sea'],
  'Tampa Bay Buccaneers': ['TB', 'Bucs', 'Buccaneers', 'TBO', 'tam', 'TAM', 'Tampa', 'Tampa Bay'],
  'Tennessee Titans': ['TEN', 'Titans', 'Tennessee', 'oti', 'ten'],
  'Washington Football Team': ['WAS', 'Redskins', 'Washington', 'was', 'Washington Redskins', 'Football Team', 'Washington FootballTeam']
}


def _standardize(item: str, mapping: dict) -> List[Tuple[str, str]]:
    """Standardizes item from mapping
    
    Args:
        item (str): the item to match
        mapping (dict): the item mapping

    Returns:
        List[Tuple[str, str]]

    """
    if item in mapping:
        return [(item, item)]
    return [(k, v) for k, v in mapping.items()
               if (item in v or
                   item.title() in v or
                   item.lower() in v or
                   item.upper() in k or
                   item.upper() in v)
           ]


def is_standardized(teams: Set[str], team_type: str = 'code') -> bool:
    """Tests if team codes are standardized
    
    Args:
        teams (Set[str]): the list of codes / names to standardize
        team_type (str): default 'code', can also be 'name'

    Returns:
        bool

    """
    if team_type == 'code':    
        return teams.issubset(standard_team_codes())
    return teams.issubset(standard_team_names())


def standard_team_codes() -> Set[str]:
    """Set of the standardized team codes
    
    Args:
        None

    Returns:
        Set[str]

    """
    return set(TEAM_CODES.keys())

    
def standard_team_names()-> Set[str]:
    """Set of the standardized team names
    
    Args:
        None

    Returns:
        Set[str]

    """
    return set(TEAM_NAMES.keys())

    
def standardize_team_code(team: str) -> str:
    """Standardizes team code across sites

    Args:
        team (str): the code or team name

    Returns:
        str: 2-3 letter team code, ATL, BAL, etc.

    Examples:
        >>>team_code('Ravens')
        'BAL'

        >>>team_code('JAC')
        'JAX'
    """
    matches = _standardize(team, TEAM_CODES)
    if not matches:
        logging.warn(f'no match for {team}')
        return team
    if len(matches) > 1:
        raise ValueError(f'too many matches for {team}:\n{matches}')    
    return matches[0][0]


def standardize_team_name(team: str) -> str:
    """Standardizes team name across sites

    Args:
        team (str): the code or team name

    Returns:
        str: team name, Atlanta Falcons, Baltimore Ravens, etc.

    """
    matches = _standardize(team, TEAM_NAMES)
    if not matches:
        logging.warn(f'no match for {team}')
        return team
    if len(matches) > 1:
        raise ValueError(f'too many matches for {team}:\n{matches}')    
    return matches[0][0]

