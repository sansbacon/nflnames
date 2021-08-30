# nflnames/tests/test_nflnames_players.py
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Eric Truett
# Licensed under the MIT License

from nflnames import *
import pytest


def test_rearrange_name():
    """Tests rearrange_name"""
    s = 'Beckham Jr., Odell'
    assert rearrange_name(s) == 'Odell Beckham Jr.'


def test_remove_chars():
    """Tests remove_chars"""
    s = 'Odell Beckham Jr.'
    assert remove_chars(s) == 'Odell Beckham Jr'
    s = "Le'Veon Bell"
    assert remove_chars(s) == 'LeVeon Bell'


def test_remove_suffixes():
    """Tests remove_suffixes"""
    s = 'Odell Beckham, Jr.'
    assert remove_suffixes(s) == 'Odell Beckham, Jr.'
    assert remove_suffixes(remove_chars(s)) == 'Odell Beckham'


def test_standardize_defense_name():
    #(s: str) -> str:
    #"""Standardizes DST name
    s = "San Francisco 49ers"
    assert standardize_defense_name(s) == 'san francisco defense'


def test_standardize_player_name():
    s = 'Henry Ruggs IV'
    assert standardize_player_name(s) == 'henry ruggs'


def test_standardize_positions():
    for s in ('DST', 'Defense', 'def'):
        assert standardize_positions(s) == 'DST'
    assert standardize_positions('qb') == 'qb'


'''
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

'''