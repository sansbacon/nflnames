# nflnames/nflnames/players.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

from pathlib import Path
import re
from typing import List, Tuple

import pandas as pd
from rapidfuzz import process, fuzz


DATADIR = Path(__file__).parent / 'data'
MASTER_PLAYERS = DATADIR / 'master_players.csv'
LEGAL_CHARS = re.compile(r'\W')
SUFFIXES = {'II', 'The Second', 'III', 'The Third', 'IV', 'The Fourth', 'Jr', 'Junior', 'Sr', 'Senior', 'Esq', 'JD', 'MD', 'PhD'}
LOWER_SUFFIXES = set([s.lower() for s in SUFFIXES])
KNOWN_DUPS = {'Michael Thomas', 'Ryan Griffin', 'Chris Jones', 'David Long', 'Tony Brown', 'Brandon Williams', 'Lamar Jackson', 'Josh Allen'}


def master_player_records():
    """The master player records
    
    Returns:
        pd.DataFrame

    """
    return pd.read_csv(MASTER_PLAYERS)    


def match_name(match: str, match_from: List[str]) -> Tuple[str, int]:
    """Finds best match from list of names
    
    Args:
        match (str): the name to match
        match_from (List[str]): the names to match from

    Returns:
        Tuple[str, int]: the match and the confidence

    """
    return process.extractOne(match, match_from, scorer=fuzz.WRatio)


def rearrange_name(s: str) -> str:
    """Converts last, first to first last
    
    Args:
        s (str): the original string

    Returns:
        str: the standardized string
    
    """
    return ' '.join(reversed([i.strip() for i in s.split(', ')]))


def remove_chars(s, keep=LEGAL_CHARS):
    """Removes all but legal characters from string"""
    return ' '.join([re.sub(keep, '', i) for i in s.split()])


def remove_suffixes(s, remove=LOWER_SUFFIXES):
    """Removes suffixes from string"""
    s = s.split()
    if s[-1].lower() in remove:
        s = s[:-1]
    return ' '.join(s)


def standardize_defense_name(s: str) -> str:
    """Standardizes DST name
    
    Args:
        s (str): the original string

    Returns:
        str: the standardized string

    """   
    return standardize_player_name(s).split()[-1] + ' defense'


def standardize_player_name(s: str) -> str:
    """Standardizes player name
    
    Args:
        s (str): the original string

    Returns:
        str: the standardized string

    """
    return re.sub(r'\s+', ' ' , remove_suffixes(remove_chars(s))).lower()


def standardize_positions(s: str) -> str:
    """Standardizes position names
    
    Args:
        s (str): the position string

    Returns:
        str: the standardized string

    """
    mapping = {'Def': 'DST', 'Defense': 'DST', 'DEF': 'DST', 'def': 'DST', 'dst': 'DST'}
    std = mapping[s] if s in mapping else s
    return std
