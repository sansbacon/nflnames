# nflnames/nflnames/players.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

from functools import lru_cache
from pathlib import Path
import re
import string

import pandas as pd


LEGAL_CHARS = re.compile(r'\W')
SUFFIXES = {'II', 'The Second', 'III', 'The Third', 'IV', 'The Fourth', 'Jr', 'Junior', 'Sr', 'Senior', 'Esq', 'JD', 'MD', 'PhD'}
LOWER_SUFFIXES = set([s.lower() for s in SUFFIXES])


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
    return ' '.join(standardize_player_name(s).split()[:-1]) + ' defense'


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
