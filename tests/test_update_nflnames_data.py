# -*- coding: utf-8 -*-
# tests/test_update_nflnames_data.py
from pathlib import Path

import requests
import pandas as pd
import pytest

from scripts.update_nflnames_data import *

def test_defense_to_dst():
    """Tests defense_to_dst"""
    col = pd.Series(['Def', 'Def', 'QB'])
    assert defense_to_dst(col).values.tolist() == ['DST', 'DST', 'QB']


def test_normalize_name():
    """Tests normalize_name"""
    pairs = (('Smith Jr., Dennis', 'smith dennis'),
             ('Greenv, V.J.', 'greenv vj'),
             ('Giants, New York', 'giants new york'),
             ('Fuller V, Will', 'fuller will'),
             ('Robinson IV, Nate', 'robinson nate'),
            )
    
    for old, new in pairs:
        assert normalize_name(old) == new


def test_fix_name():
    """Tests fix_name"""
    names = ['Smith Jr., J.R.', 'Bills, Buffalo', 'Brady, Tom']
    pos = ['WR', 'DST', 'QB']
    df = pd.DataFrame({'position': pos, 'name_': names})
    df['name_norm'] = df.apply(fix_name, axis=1)
    newnames = df.loc[:, 'name_norm'].values.tolist()
    assert newnames == ['jr smith', 'bills defense', 'tom brady']

    # test column arg
    names = ['Smith Jr., J.R.', 'Bills, Buffalo', 'Brady, Tom']
    pos = ['WR', 'DST', 'QB']
    df = pd.DataFrame({'position': pos, 'name_norm': names})
    df['name_norm'] = df.apply(fix_name, args=('name_norm', ), axis=1)
    newnames = df.loc[:, 'name_norm'].values.tolist()
    assert newnames == ['jr smith', 'bills defense', 'tom brady']


def test_update_data(test_directory):
    url = 'https://raw.githubusercontent.com/sansbacon/nflnames-data/main/players/mfl_players.json'
    data = requests.get(url).json()
    df = pd.DataFrame(data['players']['player'])
    df = clean_mfl_players(df)
    csvpth = test_directory / 'mfl_players.csv'
    df.to_csv(csvpth, index=False)
    assert csvpth.is_file()

